# -*- coding: utf-8 -*-
"""
Created on Tue Sep 12 20:39:09 2017

"""
from __future__ import print_function
import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import load_boston
import scipy.misc as mis

np.random.seed(0)

# load boston housing prices dataset
boston = load_boston()
x = boston['data']
N = x.shape[0]
x = np.concatenate((np.ones((506, 1)), x), axis=1)  # add constant one feature - no bias needed
d = x.shape[1]
y = boston['target']

idx = np.random.permutation(range(N))


# helper function
def l2(A, B):
    '''
    Input: A is a Nxd matrix
           B is a Mxd matirx
    Output: dist is a NxM matrix where dist[i,j] is the square norm between A[i,:] and B[j,:]
    i.e. dist[i,j] = ||A[i,:]-B[j,:]||^2
    '''
    A_norm = (A ** 2).sum(axis=1).reshape(A.shape[0], 1)
    B_norm = (B ** 2).sum(axis=1).reshape(1, B.shape[0])
    dist = A_norm + B_norm - 2 * A.dot(B.transpose())
    return dist


# A helper work on formula from q2.1, generate w^*
def formula_w(x_train, y_train, lam, A):
    # All formulas below are all according to assignment handout.

    # (The transpose of x_train dot product A) = temp, which is (X^Y)A in handout.
    temp = np.dot(x_train.T, A)

    # (X^Y)AX in handout
    element1 = np.dot(temp, x_train)
    # (X^Y)Ay in handout
    element2 = np.dot(temp, y_train)

    # np.eye will return a 2-D array with ones on the diagonal and zeros elsewhere.
    # I is an array where all elements are equal to zero.
    I = np.eye(element1.shape[0])

    # λI in handout
    element3 = lam * I

    # (X^Y)AX + λI in handout
    element4 = element1 + element3

    # similar to q1
    # handout formular is w^* = (((X^T)AX + λI)^(-1))((X^T)Ay)
    # which can be show as "w^* = (a^(-1))b" or "a(w^*) = b"
    # at here, element4 = a = (X^T)AX + λI, element2 = b = (X^T)Ay
    # so use np.linalg.solve to w^* as well as q1
    w = np.linalg.solve(element4, element2)

    return w


# A helper work on formula from q2.2, generate A, A_ii = a^(i)
def formula_ai(test_datum, x_train, tau):
    # All formulas below are all according to assignment handout.

    # Call helper function l2 to get matrix dist with test_datum and x_train
    dist = l2(test_datum, x_train)

    # np.divide(x1, x2) can divide arguments element-wise and return x1/x2.
    # Returns a scalar if both x1 and x2 are scalars.
    # "-1 * (l2(test_datum, x_train))" is the Dividend array.
    # "2 * tau * tau" is the Divisor array.
    array = np.divide(-1 * dist, 2 * tau * tau)

    # Compute the log of the sum of exponentials of input elements.
    sum_log = mis.logsumexp(array)

    # Calculate the exponential of all elements in the input array and get a output array,
    # element-wise exponential of array.
    exp1 = np.exp(array)
    exp2 = np.exp(sum_log)

    # Compute distance-based weights for each training example as assignment handout.
    A = np.divide(exp1, exp2)

    return A


# to implement
def LRLS(test_datum, x_train, y_train, tau, lam=1e-5):
    '''
    Input: test_datum is a dx1 test vector
           x_train is the N_train x d design matrix
           y_train is the N_train x 1 targets vector
           tau is the local reweighting parameter
           lam is the regularization parameter
    output is y_hat the prediction on test_datum
    '''
    ## TODO

    # All formulas below are all according to assignment handout and lecture slides.

    A = formula_ai(np.array([test_datum]), x_train, tau)

    # Extract a diagonal array.
    A = np.diag(A[0, :])

    w = formula_w(x_train, y_train, lam, A)

    # predict on test_datum
    y_hat = np.dot(test_datum, w)

    return y_hat

    ## TODO


def run_validation(x, y, taus, val_frac):
    '''
    Input: x is the N x d design matrix
           y is the N x 1 targets vector
           taus is a vector of tau values to evaluate
           val_frac is the fraction of examples to use as validation data
    output is
           a vector of training losses, one for each tau value
           a vector of validation losses, one for each tau value
    '''
    ## TODO

    # randomly permute np.arange(range(data_num)) as random index array
    # idx = np.random.permutation(range(N))

    # Also, it is OK if use global or local idx here.
    # There result will be slightly diffterent, but the trend is the same.
    shuffled_x = x[idx]
    shuffled_y = y[idx]

    index = int(N * (1 - val_frac))

    x_training_data = shuffled_x[:index]
    x_validation_data = shuffled_x[index:]

    y_training_data = shuffled_y[:index]
    y_validation_data = shuffled_y[index:]

    # init data sets
    training_losses = np.zeros(len(taus))
    validation_losses = np.zeros(len(taus))

    y_training_losses = np.zeros(len(y_training_data))
    y_validation_losses = np.zeros(len(y_validation_data))

    # training
    training_tau_counter = 0

    for tau in taus:

        counter = 0

        for datum, target in zip(x_training_data, y_training_data):
            squared_loss = 0.5 * ((LRLS(datum, x_training_data, y_training_data, tau) - target) ** 2)
            y_training_losses[counter] = squared_loss
            counter += 1

        average = sum(y_training_losses) / len(y_training_losses)
        training_losses[training_tau_counter] = average
        training_tau_counter += 1

    # validation
    validation_tau_counter = 0

    for tau in taus:

        counter = 0

        for datum, target in zip(x_validation_data, y_validation_data):
            squared_loss = 0.5 * ((LRLS(datum, x_training_data, y_training_data, tau) - target) ** 2)
            y_validation_losses[counter] = squared_loss
            counter += 1

        average = sum(y_validation_losses) / len(y_validation_losses)
        validation_losses[validation_tau_counter] = average
        validation_tau_counter += 1

    return training_losses, validation_losses

    ## TODO


if __name__ == "__main__":
    # In this excersice we fixed lambda (hard coded to 1e-5) and only set tau value. Feel free to play with lambda as well if you wish
    taus = np.logspace(1.0, 3, 200)
    train_losses, test_losses = run_validation(x, y, taus, val_frac=0.3)
    plt.semilogx(taus,train_losses)
    plt.semilogx(taus,test_losses)
    plt.xlabel('Tau')
    plt.ylabel('Average Loss')
    plt.show()
