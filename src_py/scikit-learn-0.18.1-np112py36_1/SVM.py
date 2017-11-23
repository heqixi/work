""" the implement the SVM algortithm
@ author :heqixi
@date：30，Setp,2017
"""
import numpy as np
from numpy import linalg
import cvxopt
import pylab as pl 
import cvxopt.solvers

def linear_kernel(x1,x2):
    return np.dot(x1,x2)


"""the polynomial_kernel funtion

    parameter
    ---------
    x1,x2:array_like,the input array 
    p : int. the parameter of the pow funtion
    """

def polynomial_kernel(x,y,p=3):
    return (1+np.dot(x,y))**p 

def gaussian_kernel(x,y,sigma = 5.0):
    return np.exp(-linalg.norm(x-y)**2/(2*(sigma**2)))

class SVM(object):
    """the class of SVM
    """
    def __init__(self,kernel= linear_kernel,c=None):
        self.kernel = kernel;
        self.c = c 
        if self.c is not None :
            self.c = float(self.c)
    
    def fit (self,X,y):
        n_samples,n_features = X.shape
        # Gausian matix 
        K = np.zeros((n_samples,n_samples))
        for i in range(n_samples):
            for j in range(n_samples):
                K[i,j] = self.kernel(X[i],X[j])
            P = cvxopt.matrix(np.outer(y,y)*K)
            q = cvxopt.matrix(np.ones(n_samples)* -1)
            A = cvxopt.matrix(y,(1,n_samples))
            b = cvxopt.matrix(0.0)

        if self.c is None:
            G = cvxopt.matrix(np.diag(np.ones(n_samples)*-1))
            h = cvxopt.matrix(np.zeros(n_samples))

        else:
            tmp1 = np.diag(np.ones(n_samples)* -1)
            tmp2 = np.identity(n_samples)
            G = cvxopt.matrix(np.vstack((tmp1,tmp2)))
            tmp1 = np.zeros(n_samples)
            tmp2 = np.ones(n_samples) * self.c 
            h = cvxopt.matrix(np.hstack((tmp1,tmp2)))
    
            # solve QP problem
        solution = cvxopt.solvers.qp(P,q,G,h,A,b)

        # Lagrange multupliers
        a = np.ravel(solution['x']) 
        sv = a > 1e-5
        ind = np.arange(len(a))[sv]
        self.a = a[sv]
        self.sv = X[sv]
        self.sv_y = y[sv]
        print("%d support vectors out of %d points" % (len(self.a ),n_samples))
         
        # Intercept
        """
        这里相当于对所有的支持向量的b求平均值
        """
        self.b = 0 
        for n in range(len(self.a)):
            self.b += self.sv_y[n]
            self.b -= np.sum(self.a * self.sv_y * K[ind[n],sv])
        self.b /= len(self.a)
        if self.kernel == linear_kernel:
            self.w = np.zeros(n_features)
            for n in range(len(sefl.a)):
                # linear_kernel 相当于在原空间，故计算w时不用映射到future space 
                self.w  = self.a[n] * self.sv_y(n) * self.sv[n]

        else:
            self.w = None 
    def project (self,X):
        if self.w is not None:
            return np.dot(X,self.w) + self.b
        else:
            y_predict = np.zeros(len(X))
            for i in range(len(X)):
                s = 0 
                for a,sv_y,sv in zip(self.a,self.sv_y,self.sv):
                    s += a* sv_y * self.kernel(X[i],sv)
                y_predict[i] = s
            return y_predict +self.b 
    def predict(self,X):
        return np.sign(self.project(X))

    def gen_lin_seperable_data(self):

        # generate trainint  data in the 2-d case 
        mean1 = np.array([0,2])
        mean2 = np.array([2,0])
        cov = np.array([[0.8,0.6],[0.6,.08]])
        X1 = np.random.multivariate_normal (mean1,cov,100)
        y1 = np.ones(len(X1))
        X2 = np.random.multivariate_normal(mean2,cov,100)
        y2 = np.ones(len(X2))
        return X1,y1,X2,y2
    def gen_non_lin_seperable_data(self):
        mean1 = [-1,2]
        mean2 = [1,-1]
        mean3 = [4,-4]
        mean4 = [-4,4]
        cov =np.array([[1.0,0.8],[0.8,1.0]])
        X1 = np.random.multivariate_normal(mean1,cov,100)
        y1 = np.ones(len(X1))
        X2 = np.random.multivariate_normal(mean2 ,cov, 100)
        y2 = np.ones(len(X2)) *-1
        return X1,y1,X2,y2
    def split_train (self,X1,y1,X2,y2):
        X1_test = X1[90:]
        y1_test = y1[90:]
        X2_test = X2[90:]
        y2_test = y2[90:]
        X_test = np.vstack((X1_test,X2_test))
        y_test = np.hstack((y1_test,y2_test))
        return X_test,y_test
    def split_test(self,X1,y1,X2,y2):
        X1_train = X1[:90]
        y1_train = y1[:90]
        X2_train = X2[:90]
        y2_train = y2[:90]
        X_train = np.vstack((X1_train,X2_train))
        y_train  = np.hstack((y1_train,y2_train))
        return X_train,y_train 
    # only plot the result in Linears,
    def plot_margin(X1_train,X2_train,clf):
        def f (x,w,b,c = 0 ):
            # given x ,return y such that [x,y] in on the line 
            # w.x + b = c 
            return (-w[0]*x - b +c ) / w[1]
        pl.plot(X1_train[:,0],X1_train[:,1],"ro")
        pl.plot(X2_train[:,0],X2_train[:,1],"bo")
        pl.scatter(clf.sv[:,0],clf.svp[:,1],s = 100 ,c = "g")

        # w .x + b = 0 
        a0 = -4 
        a1 = f(a0,clf.w ,clf.b)
        b0 = 4
        b1 = f(b0 ,clf.w,clf.b)
        pl.plot([a0,b0],[a1,b1],"k")

        # w.x + b = 1 
        a0 = -4 
        a1 = f(a0,clf.w,clf.b,1)
        b0 = 4 
        b1 = f(b0,clf.w,clf.b,1)
        pl.plot([a0,b0],[a1,b1],"k--")

        # w.x + b = -1 
        a0 = 4
        a1 =f(a0,clf.w,clf.b,-1)
        b0 = 4 
        b1 = f(b0,clf.w,clf.b,-1)
        pl.plot([a0,b0],[a1,b1],"k--")

        pl.axis("tight")
        pl.show ()

    def plot_contour(self,X1_train,X2_train,clf):
        # plot the figure of training samples
        pl.plot(X1_train[:,0],X1_train[:,1],"ro")
        pl.plot(X2_train[:,0],X2_train[:,1],"bo")
        #做support vectors 的图
        pl.scatter(clf.sv[:,0],clf.sv[:,1],s = 100,c ="g")
        X1,X2 = np.meshgrid(np.linspace(-6,6,50),np.linspace(-6,6,50))
        X = np.array([[x1,x2] for x1,x2 in zip(np.ravel(X1),np.ravel(X2))])
        Z = clf.project(X).reshape(X1.shape)
        # pl.contour 做等值图 

        pl.contour(X1,X2,Z,[0.0],colors="k",linewiths = 1,gin = 'lower')
        pl.contour(X1,X2,Z+1,[0.0],colors = 'grey',linewiths = 1,gin = 'lower')
        pl.contour(X1,X2,Z-1,[0.0],colors = 'grey',linewiths = 1 ,gin = 'lower')
        pl.axis = ("tight")
        pl.show()
    def test_linear():
        X1,y1,X2,y2 = self.gen_lin_seperable_data()
        X_train,y_train = split_train(X1,y1,X2,y2)
        X_test ,y_test = split_test(X1,y1,X2,y2)
        clf = SVM()
        clf.fit(X_train,y_train)
        y_predict = clf.predict(X_test)
        correct = np.sum(y_predict == y_test )
        print ("%d out of %d predictions correct" % (correct,len(y_predict))) 

        plot_margin(X_train[y_train ==1 ],X_train[y_train == -1],clf)
    def test_non_linear(self):
        X1,y1,X2,y2 =self.gen_non_lin_seperable_data()
        X_train,y_train =self.split_train(X1,y1,X2,y2)
        X_test,y_test = self.split_test(X1,y1,X2,y2)

        clf = SVM(gaussian_kernel)
        clf.fit(X_train,y_train)
        y_predict = clf.predict(X_test)
        correct = np.sum(y_predict == y_test)
        print("%d out of %d prediction correct"% (correct,len(y_predict)))
        self. plot_contour(X_train[y_train == 1],X_train[y_train == -1],clf)


    def test_soft():
        X1,y1,X2,y2 = gen_lin_seperable_data()
        X_train,y_train = split_train(X1,y1,X2,y2)
        X_test,y_test = split_test(X1,y1,X2,y2)

        clf = SVM (C = 0.1)
        clf.fit(X_train,y_train)
        y_predict = clf.predict(X_test)
        correct = np.sum(y_predict == y_test)
        print ( "%d out of %d predictions correct "% (correct,len(y_predict)))

        plot_contour(X_train[y_train == 1],X_train[y_train == -1],clf)

my_svm = SVM("linear_kernel")
my_svm.test_non_linear()
