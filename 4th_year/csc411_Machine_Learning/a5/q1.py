'''
Question 1 Skeleton Code

Here you should implement and evaluate the Conditional Gaussian classifier.
'''

import data
import numpy as np
# Import pyplot - plt.imshow is useful!
import matplotlib.pyplot as plt


def compute_mean_mles(train_data, train_labels):
    '''
    Compute the mean estimate for each digit class

    Should return a numpy array of size (10,64)
    The ith row will correspond to the mean estimate for digit class i
    '''
    means = np.zeros((10, 64))
    # Compute means
    for i in range(0, 10):
        means[i, :] = np.mean(data.get_digits_by_label(train_data, train_labels, i), axis=0)
    return means


def compute_sigma_mles(train_data, train_labels):
    '''
    Compute the covariance estimate for each digit class

    Should return a three dimensional numpy array of shape (10, 64, 64)
    consisting of a covariance matrix for each digit class
    '''
    covariances = np.zeros((10, 64, 64))
    # Compute covariances
    means = compute_mean_mles(train_data, train_labels)

    for i in range(0, 10):
        for j in range(0, 64):
            for k in range(0, 64):

                digit = data.get_digits_by_label(train_data, train_labels, i)
                if np.shape(np.transpose(digit[:, j]))[0] == np.shape(np.transpose(digit[:, k]))[0]:
                    total = np.dot((np.transpose(digit[:, j]) - means[i, j]),
                                   (np.transpose(np.transpose(digit[:, k]) - means[i, k])))
                    covariances[i, j, k] = total / (np.shape(np.transpose(digit[:, j]))[0])

        covariances[i] = covariances[i] + np.identity(64) * 0.01

    return covariances


def generative_likelihood(digits, means, covariances):
    '''
    Compute the generative log-likelihood:
        log p(x|y,mu,Sigma)

    Should return an n x 10 numpy array
    '''

    n = digits.shape[0]
    result = np.zeros((n, 10))

    for n in range(n):
        for i in range(10):
            delta = (digits[n] - means[i]).reshape(64, -1)
            result[n][i] = (-digits.shape[1] / 2 * np.log(2 * np.pi)) + \
                           (-0.5 * np.log(np.linalg.det(covariances[i]))) + \
                           (-0.5 * np.dot(np.dot(delta.T, np.linalg.inv(covariances[i])), delta))
    return result


def conditional_likelihood(digits, means, covariances):
    '''
    Compute the conditional likelihood:

        log p(y|x, mu, Sigma)

    This should be a numpy array of shape (n, 10)
    Where n is the number of datapoints and 10 corresponds to each digit class
    '''
    first = np.exp(generative_likelihood(digits, means, covariances))
    second = 1 / 10
    third = np.sum(first * second, axis=1).reshape(-1, 1)
    return np.log(first) + np.log(second) - np.log(third)


def avg_conditional_likelihood(digits, labels, means, covariances):
    '''
    Compute the average conditional likelihood over the true class labels

        AVG( log p(y_i|x_i, mu, Sigma) )

    i.e. the average log likelihood that the model assigns to the correct class label
    '''
    cond_likelihood = conditional_likelihood(digits, means, covariances)
    n = digits.shape[0]
    total = 0
    for i in range(n):
        correct = int(labels.item(i))
        total += cond_likelihood[i, correct]
    return total / n


def classify_data(digits, means, covariances):
    '''
    Classify new points by taking the most likely posterior class
    '''
    cond_likelihood = conditional_likelihood(digits, means, covariances)
    # Compute and return the most likely class

    n = digits.shape[0]
    predictions = np.zeros((n, 1))
    for i in range(n):
        predictions[i] = np.where(cond_likelihood[i] == cond_likelihood[i].max())
    return predictions


def plot_cov_eigenvectors(covariances):
    eigenvecs = np.zeros((10, 8, 8))

    for i in range(10):
        val, vec = np.linalg.eig(covariances[i])
        eigenvecs[i] = vec[:, np.argmax(val)].reshape(8, 8)

    all_concat = np.concatenate(eigenvecs, 1)
    plt.imshow(all_concat, cmap='gray')
    plt.show()


def accuracy(labels, predictions):
    count = 0
    n = predictions.shape[0]
    for i in range(n):
        if int(predictions[i]) == int(labels[i]):
            count += 1
    return count / n


def main():
    train_data, train_labels, test_data, test_labels = data.load_all_data('data')

    # Fit the model
    means = compute_mean_mles(train_data, train_labels)
    covariances = compute_sigma_mles(train_data, train_labels)
    test_cov = compute_sigma_mles(test_data, test_labels)

    # Evaluation
    plot_cov_eigenvectors(covariances)
    plot_cov_eigenvectors(test_cov)

    train_avg = avg_conditional_likelihood(train_data, train_labels, means, covariances)
    test_avg = avg_conditional_likelihood(test_data, test_labels, means, covariances)

    print("Training set average conditional likelihood: ", train_avg)
    print("Testing set average conditional likelihood: ", test_avg)

    train_predict = classify_data(train_data, means, covariances)
    test_predict = classify_data(test_data, means, covariances)

    train_acc = accuracy(train_labels, train_predict)
    test_acc = accuracy(test_labels, test_predict)

    print("Training set accuracy: ", train_acc)
    print("Testing set accuracy: ", test_acc)


if __name__ == '__main__':
    main()
