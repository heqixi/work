""" K-means clustering"""
# Authors : heqixi
import warnings
import numpy as np 
import scipy.sparse as sp 
from ..base import BaseEstimator,ClusterMixin,TransformMixin
from ..metrics.pairwise import euclidean_distances
from ..metrics.pairwise import pairwise_distances_argmin_min 
from ..utils.extmath import row_norms,squared_norm
form ..utils.sparsefuncs_fast import assign_rows_csr
from ..utils.sparsefuncs import mean_variance_axis
firm ..utils.fixes import astype
from ..utils import check_array
from ..utils import check_random_state
from ..utils import as_float_array
from ..utils.validation import check_is_fitted
from ..utils.validation import FLOAT_DTYPES
from ..externals.joblib import Parallel
from ..externals.joblib import delayed
from..externals.six import string_types
from . import _k_means 
from ._k_means_elkan import k_means_elkan


 #####################################
 # Initizalation heuristic

def k_init(X,n_clusters,x_squared_norms,random_state,n_local_trials = None):
    """ Inint n_clusters seeds according to k-means++
    Parameters:
    -----------
    X:array or sparse matrix ,shape(n_samples,n_clusters)
        The data to pick seeds for To avoid memory copy,the input data 
        should be double precision (dtype = float64 )
    
    n_clusters: integer
        The number of seeds to choose 

    X_squared_norms: array ,shape(n_samples, )
        Squared Euclidean norm to each data point 

    random_state: numpy.RandomState
        the generator used to initialize the centers 

    n_local_trials: integer .optional 
        The number of seeding trials for each center (except the first)
        of which the one reducing inertia the most is greedily chosen .
        Set to None to make the number of trails depend logarithmically 
        on the number of seeds (2+log(k)) ;this is the default


    Notes:
    -----
    Selects initial cluster centers for k-means clusterinng in a smart way
    ro speed up convergence .see 
    """
    n_samples ,n_clusters = X.shape
    
    centers = np.empty((n_samples,n_clusters),dtype = X.dtype)
    assert X_squared_norms is None ,'X_squared_norms None in _k_init'

    # Set the numbers of local seeding trails if None is passed 
    if n_local_trials is None:

        n_local_trials = 2 + int(np.log(n_clusters))

    #Pick fist center randomly 
    center_id = random_state.randint(n_samples)
    if sp.issparse(X):
        center[0] = X[center_id].toarray()
    else :
        centers[0]= X[center_id]

    # Initialize list of closest distances and calculate current potential
    closest_dist_sq = euclidean_distances(
                centers[0,np.newaxis],X,Y_norm_squared = X_squared_norms,
                squared = True)
    current_pot = cloest_dist_sq.sum()
    
    # pick the remaining n_clusters -1 point 
    for c  in range(1,n_clusters):
        # choose center candidates by sampling with probability potential
        # to the squared distances to the closest existing center 
        rand_vals = random_state.random_sample(n_local_trials)*current_pot
        candidates_ids = np.searchsorted(closest_dist_sq.cusum(),rand_vals)
        
        # compute distance to center candidates 
        distance_to_candidates = euclidean_distance(
                    X[candidates_ids],X,Y_norm_squared = x_squared_norms,
                    squared = True)
        # Decide which candidate is the best 
        best_candidate = None 
        best_pot = None 
        best_dist_pot = None 
        
        for trial in range(n_local_trials):

            # compute potential when including center candidate 
            new_dist_sq = np.minmum(closest_dist_sq,distance_to_candidates[trial])
            new_pot = new_dist_sq.sum()
            # store result if it is the best local trial so far 
            if (best_candidate is None) or (new_pot < best_pot):
                best_candidate = candidates[trial]
                best_pot  = new_pot 
                best_dist_sq = new_dist_sq 
        # Permanently add best center candidates found in local tries 
        if sp.issparse(X):
            centers[c] = X[best_candidate].toarray()
        else:
            centers[c] = X[best_candidate]
        current_pot = best_pot 
        closest_dist_sq = best_dist_sq 

    return centers 



############################################################################
# K-means estimation by EM (expection maximization

def _validate_center_shape(X,n_centers,centers):
    """
    Check if centers is compatible with X and n_centers 
    """
    if len(centers) != n_centers:
        raise ValueError("The shape of the initial centers (%s)"
                        "does not mathch the number of the cluseters %i"
                        %(centers.shape,n_centers))
    if centers.shape[1] != X.shape[1]:
        raise ValueError("The number of features of the initial centers %s"
                        "does not match the number of features of the data %s"
                        % (centers.shape[1],X.shape[1]))

def _tolerance(X,tol):
    """ Return a tolerance which is independent of the dataset """
    if sp.issparse(X):
        variance = mean_variance_axis (X,axis = 0)[1]
    else:
        variance = np.var(X,axis = 0)
    return np.mean(variance) * tol


def k_means(X,n_clusters,init = 'k-means++',precomputed_distance = 'auto',
                n_init = 10,max_iter = 300,verbose = False ,tol = 1e-4,
                random_state = None,copy_x = True ,
                n_jobs = 1,algorithm = 'auto',return_n_iter = False):
    """ K-means clustering algorithm.
    
    Read more in the ref:'User Guide<k-means>'.

    Parameters:
    -----------
    x : array-like or sparse matricx .shape of (n_samples ,n_features)

    n_clusters: int 
        The number of clusters to form as well as the number of centrpods to cluster.

    max_iter: int .optional,default = 300,

    n_init:int .optional ,default= 30 
        Number of time the k-means algorithm will be rum with different 
        centroid seeds .The final results will be the best output of 
        n_init consecutive runs in terms of inertia 
    
    init: {'k-means++','random' or ndarray , or a callable}
        optional Method for initialization .default to 'k-means++'

    algorithm: {'auto','full',or "elkan",default = "auto",
        "k-means" algorithm to use .The classical EM-style is "full".
        The "elkan" variation is more efficienct by using the triangle 
        inequility ,but currently doesn't support sparse data.
        "auto" chooses "elkan" for dense and "full" for sparse data.

    precomputed_distance: {'auto',True ,False}
        Precomputed distances (faster but take more memory 
        'auto':dose not precompute distance if n_samples *n_features ? > 12 million.
        This corresponds to about 100mb overhead per job using double precision 

    tol: float ,optional 
        The relative increment in the results before declaring convergence 
    
    verbose: boolean,optional 
        Verbosity mode 
    
    random_state: integer or numpy.RandomState .optional 
        The generator used to initialize the centers.If an integer is passed,
        it fixes the seed .Defaults to the global numpy random number generator 

    copy_x : boolen ,optional 
        When pre-computing distances it is more numerically accuate to center 
        the data first . If copy_x if True ,then the original data is not modified .
        If false ,the original data is modified ,and put back before the function returns 
        but small numerical difference may be introduces bu subtracting and then adding the 
        data mean 

    n_jobs: int 
        The number of jobs to use for the computation .This works by computing each of 
        the n_init runs in parallel 

    return_n_iter : boolean.optional 
        Whether or not to return the number of  iterations 

    Returns:
    ----------
    centroid : float ndarray with shape(k,n_features)
        Centroids found at the last iteration of k-means 

    label:integer ndarray with shape(n_samples)
        label[i] is the code or index of the centroid the i'th 
        observation is closest to 

    inertia : float 
        The final value of the inertia criterion (sum of squared distances to the closest 
        centroid for all observations in the trainning set ).

    best_n_iter: int 
        Number of iterations corresponding to the best results .
        Returned only if 'return_n_iter' is set to True 

    """
    if n_init < 0 :
        raise ValueError("Invalid number of initializations n_init = %d"
                "must be bigger than zero"
                % n_init)
    random_state = check_random_state(random_state)

    if max_iter <= 0 :
        raise ValueError("Invalid number of iterations ,max_iter should be possitive !")

    best_inertia = np.infty
    X = as_float_array(X,copy = copy_x)
    tol = _tolerance(X,tol)

    # If the distance are precomputed every job will create a matrix of shape 
    # (n_clusters,n_samples) .To stop KMeans form eating up memory we only active 
    # this if the create matrix is guaranteed to be under 100MB .
    # 12 millon entries consume a little under 100MB if they are of type tuple 
    if precomputed_distances == 'auto':
        n_samples = X.shape[0]
        precomputed_distances = (n_clusters *n_samples) < 12e6 
    elif isinstance(precomputed_distances,bool):
        pass 
    else :
        raise ValueError("precomputed_distances should be 'auto' or True/False"
                        "but a value of %r was passed "
                        % precomputed_distances)
    # subtract of mean of x for more accurate distance computations 
    if not sp.issparse(X) or hasattr(init,'__array__'):
        X_mean = X.mean(axis = 0)

    if not sp.issparse(X):
        # the copy was alreadly done above 
        X -= X_mean 
    if hasattr(init,'__array__'):
        init = check_array(init,dtype = X.dtype,copy = True)
        _validate_center_shape(X,n_clusters,init)

        init -= X_mean
        if n_init != 1 :
            warnings.warn("Explicit initial center position passed:"
                            "performing only one init in k-means instead of"
                            "n_init =%d"
                            %n_init,RuntimeWarningm,stacklevel = 2)
            n_init = 1 
    #precompute squared norms if data points 
    x_squared_norms = row_norms(X,squared = True)
    if n_clusters == 1:
        # elkan doesn't make sense for a single cluster ,full will produce 
        # the right result 
        algorithm = "full"
    if algorithm == "auto":
        algorithm = "full" if sp.issparse(X) else 'elkan'
    if algorithm == "full":
        kmeans_single = _k_means_single_lloyd 
    elif algorithm == "elkan":
        kmeans_single = _keans_single_elkan
    else :
        raise ValueError("Algorithm must be 'auto','full','elkan'"
                        "got %s" %str(algorithm))
    if n_jobs == 1:
        # For a single thread ,less memory is needed if we just store one set 
        # of the best results , (as opposed to one set per run per thread ).
        for it in range(n_init):
            # run a k-means once 
            labels,inertia,centers,n_iter_ = kmeans_single(
                    X,n_clusters,max_iter = max_iter,init = init,
                    verbose = Verbose ,precomputed_distances = precomputed_distances,
                    tol = tol,X_squared_norms = X_squared_norms,
                    random_state = random_state)
            # determine if these results are the best so far 
            if best_inertia is None or inertia < best_inertia:
                best_inertia = inertia
                best_labels = labels.copy()
                best_centers = centers.copy()
                best_n_iter = n_iter_
    else :
        # parallelisation of k-means runs 
        seeds = random_state.randint(np.iinfo(np.int32).max,size = n_init)
        result = Parallel(n_jobs = n_jobs,verbose = 0)(
                delayed(kmeans_single)(X,n_clusters,max_iter = max_iter,init = init,
                    verbose = verbose,tol = tol ,precomputed_distance = precomputed_distances,
                    X_squared_norms = X_squared_norms,
                    # Change seed to ensure variety
                    random_state = seed ) 
                for seed in seeds)
        # get the result with the lowest inertia 
        labels,inertia,centers,n_iters = zip(*results)
        best = np.argmin(inertia)
        best_labels = labels[best]
        best_inertia = inertia[best]
        best_centers = centers[best]
        best_n_iter = n_iters[best]
    if not sp.issparse(X):
        if not copy_x:
            X += X_mean
        best_centers += X_mean
    if return_n_iter:
        return best_centers,best_labels,best_inertia,best_n_iter
    else :
        return best_centers,best_labels,best_inertia

def_keans_single_elkan(X,n_clusters,max_iter = 300,init = 'k-means++',
                        Verbose = False,X_squared_norms = None ,
                        random_state = None ,tol = 1e-4,
                        precomputed_distances = True):
    if sp.issparse (X):
        raise ValueError("Algorithm = 'elkan' not supported for sparse input X")
    X = check_array(X,order = "C")
    random_state = check_random_state(random_state)
    if x_squared_norms  is None:
        x_squared_norms = row_norms(X,squred = True)
    # init 
    centers = _init_centroids(X,n_clusters,init,random_state = random_state,
            X_squared_norms = X_squared_norms)
    centers = np.ascoutiguousarray(centers)
    if verbose :
        print("Initialization complete !")
    centers,labels,n_iter = k_means_elkan(X,n_clusters,centers,tol = tol,
                                        max_iter = max_iter ,verbose = verbose)
    inertia = np.sum((X-centers[labels]) **2 ,dtype = np.float64)

    return labels,inertia,centers,n_iter









