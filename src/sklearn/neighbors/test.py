import numpy as np 
from sklearn.neighbors import NearestNeighbors
samples = [[0., 0., 0.], [0., .5, 0.], [1., 1., .5]]
neigh = NearestNeighbors(n_neighbors=1)
neigh.fit(samples)
print(neigh.kneighbors([[1., 1., 1.]]))