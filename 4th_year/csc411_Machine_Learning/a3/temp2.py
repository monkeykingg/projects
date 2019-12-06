'''
Michael Dimmick
hw3
Q2
CSC2515
'''

from __future__ import print_function
import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import load_boston
from scipy.misc import logsumexp

np.random.seed(1337)

# load boston housing prices dataset
boston = load_boston()
x = boston['data']
N = x.shape[0]
x = np.concatenate((np.ones((506,1)),x),axis=1) #add constant one feature - no bias needed
d = x.shape[1]
y = boston['target']

#helper function
def l2(A,B):
    '''
    Input: A is a Nxd matrix
           B is a Mxd matirx
    Output: dist is a NxM matrix where dist[i,j] is the square norm between A[i,:] and B[j,:]
    i.e. dist[i,j] = ||A[i,:]-B[j,:]||^2
    '''
    A_norm = (A**2).sum(axis=1).reshape(A.shape[0],1)
    B_norm = (B**2).sum(axis=1).reshape(1,B.shape[0])
    dist = A_norm+B_norm-2*A.dot(B.transpose())
    return dist

# compute symmetric A matrix using logsumexp
def compute_dist_based_weights(test_datum,x_train,tau):
    numerator = l2(test_datum,x_train)[0]/(-2*tau**2)
    B = np.max(numerator)
    a = np.exp(np.subtract((numerator - B), logsumexp(numerator - B)))
    A = np.diag(a)
    return A

# solve linear system of equations for optimal w
def compute_optimal_w(x_train,y_train,A,lam):
    a = np.matmul(np.matmul(np.transpose(x_train),A),x_train) + lam*np.eye(d,d)
    b = np.matmul(np.matmul(np.transpose(x_train),A),y_train)
    w = np.array([np.linalg.solve(a, b)])
    return w

# compute prediction for LRLS
def LRLS(test_datum,x_train,y_train,tau,lam=1e-5):
    '''
    Input: test_datum is a dx1 test vector
           x_train is the N_train x d design matrix
           y_train is the N_train x 1 targets vector
           tau is the local reweighting parameter
           lam is the regularization parameter
    output is y_hat the prediction on test_datum
    '''
    A = compute_dist_based_weights(np.array([test_datum]),x_train,tau)
    w = compute_optimal_w(x_train,y_train,A,lam)
    prediction = np.dot(test_datum,np.transpose(w))[0]
    return prediction

# shuffle and then split the dataset
def shuffle_split(x,y,split_percent):
    idx = np.random.permutation(range(N))
    shuffled_x = x[idx]
    shuffled_y = y[idx]

    slice_index = int(N*split_percent)
    x_val = shuffled_x[:slice_index]
    x_train = shuffled_x[slice_index:]

    y_val = shuffled_y[:slice_index]
    y_train = shuffled_y[slice_index:]

    return x_train, y_train, x_val, y_val

# calcualte losses for a given dataset
def calculate_losses(x_test, y_test, x_train, y_train, taus):
    tau_losses = np.zeros(len(taus))
    dataset_losses = np.zeros(len(y_test))

    tau_counter = 0
    for tau in taus:
        test_datum_counter = 0
        for test_datum, test_label in zip(x_test, y_test):
            prediction = LRLS(test_datum, x_train, y_train, tau)
            residual = (prediction - test_label)
            loss = 0.5*(residual**2)
            dataset_losses[test_datum_counter] = loss
            test_datum_counter += 1
        tau_losses[tau_counter] = sum(dataset_losses)/len(dataset_losses)
        tau_counter += 1
    return tau_losses


# validation
def run_validation(x,y,taus,val_frac):
    '''
    Input: x is the N x d design matrix
           y is the N x 1 targets vector
           taus is a vector of tau values to evaluate
           val_frac is the fraction of examples to use as validation data
    output is
           a vector of training losses, one for each tau value
           a vector of validation losses, one for each tau value
    '''
    x_train, y_train, x_val, y_val = shuffle_split(x,y,val_frac)
    train_losses = calculate_losses(x_train, y_train, x_train, y_train, taus)
    val_losses = calculate_losses(x_val, y_val, x_train, y_train, taus)
    return train_losses, val_losses

if __name__ == "__main__":
    # In this excersice we fixed lambda (hard coded to 1e-5) and only set tau value. Feel free to play with lambda as well if you wish
    taus = np.logspace(1,3,num=100)
    train_losses, test_losses = run_validation(x,y,taus,val_frac=0.3)
    plt.semilogx(taus,train_losses)
    plt.xlabel('Tau')
    plt.ylabel('Average Training Loss')
    plt.title('Training Losses vs. Tau')
    plt.show()
    plt.semilogx(taus,test_losses)
    plt.xlabel('Tau')
    plt.ylabel('Average Validation Loss')
    plt.title('Validation Losses vs. Tau')
    plt.show()
