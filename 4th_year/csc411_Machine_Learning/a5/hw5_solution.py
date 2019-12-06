        '''
    Question 1 Solution

    Implement and evaluate the Conditional Gaussian classifier.
    '''

    import data
    import numpy as np
    import scipy.special
    # Import pyplot - plt.imshow is useful!
    import matplotlib.pyplot as plt

    def compute_mean_mles(train_data, train_labels):
        '''
        Compute the mean estimate for each digit class

        Should return a numpy array of size (10,64)
        The ith row will correspond to the mean estimate for digit class i
        '''
	# Initialize array to store means
        means = np.zeros((10, 64))
        # Compute means
        for i in range(10):
            sample = data.get_digits_by_label(train_data, train_labels, i)
            means[i] = np.mean(sample, 0)
        return means

    def compute_sigma_mles(train_data, train_labels):
        '''
        Compute the covariance estimate for each digit class

        Should return a three dimensional numpy array of shape (10, 64, 64)
        consisting of a covariance matrix for each digit class
        '''
	# Initialize array to store covariances
        covariances = np.zeros((10, 64, 64))
        # Compute covariances
        for i in range(10):
            sample = data.get_digits_by_label(train_data, train_labels, i)
            m = np.mean(sample, 0)
            cov_sum = [np.outer(s-m,s-m) for s in sample]
            cov = np.mean(cov_sum, 0)
            cov_adj = cov + (0.01 * np.eye(64))
            covariances[i] = cov_adj

        return covariances

    def generative_likelihood(digits, means, covariances):
        '''
        Compute the generative log-likelihood:
            log p(x|y,mu,Sigma)

        Should return an n x 10 numpy array
        '''
        log_2pi = np.log(2 * np.pi)
        det_array = np.linalg.det(covariances)
        log_det_array = -0.5 * np.log(det_array)
        inv_array = np.linalg.inv(covariances)

        return np.array([[-32 * log_2pi + log_det_array[i] + (-0.5 * (x-means[i]).T.dot(inv_array[i]).dot(x-means[i])) for i in range(10)] for x in digits])


    def conditional_likelihood(digits, means, covariances):
        '''
        Compute the conditional likelihood:

            log p(y|x, mu, Sigma)

        This should be a numpy array of shape (n, 10)
        Where n is the number of datapoints and 10 corresponds to each digit class
        '''
        gen_l = generative_likelihood(digits, means, covariances)
        denom = scipy.special.logsumexp(gen_l + np.log(0.1), 1)
        denom_expanded = np.array([denom] * 10).T

        return gen_l + np.log(0.1) - denom_expanded

    def avg_conditional_likelihood(digits, labels, means, covariances):
        '''
        Compute the average conditional likelihood over the true class labels

            AVG( log p(y_i|x_i, mu, Sigma) )

        i.e. the average log likelihood that the model assigns to the correct class label
        '''
        cond_likelihood = conditional_likelihood(digits, means, covariances)

        # Compute as described above and return
        assert len(digits) == len(labels)
        sample_size = len(digits)
        total_prob = 0
        for i in range(sample_size):
            total_prob += cond_likelihood[i][int(labels[i])]

        return total_prob/sample_size


    def classify_data(digits, means, covariances):
        '''
        Classify new points by taking the most likely posterior class
        '''
        cond_likelihood = conditional_likelihood(digits, means, covariances)
        # Compute and return the most likely class
        pred = np.argmax(cond_likelihood, 1)
        return pred

    def main():
        train_data, train_labels, test_data, test_labels = data.load_all_data('data')

        # Fit the model
        means = compute_mean_mles(train_data, train_labels)
        covariances = compute_sigma_mles(train_data, train_labels)

        # Evaluation
        train_log_llh = avg_conditional_likelihood(train_data, train_labels, means, covariances)
        test_log_llh = avg_conditional_likelihood(test_data, test_labels, means, covariances)

        print('Train average conditional log-likelihood: ', train_log_llh)
        print('Test average conditional log-likelihood: ', test_log_llh)

        train_posterior_result = classify_data(train_data, means, covariances)
        test_posterior_result = classify_data(test_data, means, covariances)

        train_accuracy = np.mean(train_labels.astype(int) == train_posterior_result)
        test_accuracy = np.mean(test_labels.astype(int) == test_posterior_result)

        print('Train posterior accuracy: ', train_accuracy)
        print('Test posterior accuracy: ', test_accuracy)

        for i in range(10):
            (e_val, e_vec) = np.linalg.eig(covariances[i])
            # In particular, note the axis to access the eigenvector
            curr_leading_evec = e_vec[:,np.argmax(e_val)].reshape((8,8))
            plt.subplot(3,4,i+1)
            plt.imshow(curr_leading_evec, cmap='gray')
        plt.show()

    if __name__ == '__main__':
        main()
