import numpy as np
from sklearn.datasets import load_boston
import matplotlib.pyplot as plt

BATCHES = 50

class BatchSampler(object):
    '''
    A (very) simple wrapper to randomly sample batches without replacement.

    You shouldn't need to touch this.
    '''

    def __init__(self, data, targets, batch_size):
        self.num_points = data.shape[0]
        self.features = data.shape[1]
        self.batch_size = batch_size

        self.data = data
        self.targets = targets

        self.indices = np.arange(self.num_points)

    def random_batch_indices(self, m=None):
        '''
        Get random batch indices without replacement from the dataset.

        If m is given the batch will be of size m. Otherwise will default to the class initialized value.
        '''
        if m is None:
            indices = np.random.choice(self.indices, self.batch_size, replace=False)
        else:
            indices = np.random.choice(self.indices, m, replace=False)
        return indices

    def get_batch(self, m=None):
        '''
        Get a random batch without replacement from the dataset.

        If m is given the batch will be of size m. Otherwise will default to the class initialized value.
        '''
        indices = self.random_batch_indices(m)
        X_batch = np.take(self.data, indices, 0)
        y_batch = self.targets[indices]
        return X_batch, y_batch


def load_data_and_init_params():
    '''
    Load the Boston houses dataset and randomly initialise linear regression weights.
    '''
    print('------ Loading Boston Houses Dataset ------')
    X, y = load_boston(True)
    features = X.shape[1]

    # Initialize w
    w = np.random.randn(features)

    print("Loaded...")
    print("Total data points: {0}\nFeature count: {1}".format(X.shape[0], X.shape[1]))
    print("Random parameters, w: {0}".format(w))
    print('-------------------------------------------\n\n\n')

    return X, y, w


def cosine_similarity(vec1, vec2):
    '''
    Compute the cosine similarity (cos theta) between two vectors.
    '''
    dot = np.dot(vec1, vec2)
    sum1 = np.sqrt(np.dot(vec1, vec1))
    sum2 = np.sqrt(np.dot(vec2, vec2))

    return dot / (sum1 * sum2)


#TODO: implement linear regression gradient
def lin_reg_gradient(X, y, w):
    '''
    Compute gradient of linear regression model parameterized by w
    '''

    # the gradient of "(y - (w^T)X)^2" is 2((X.T)Xw - (X.T)y)

    # (X.T)X
    element1 = np.dot(X.T, X)

    # (X.T)y
    element2 = np.dot(X.T, y)

    #(X.T)Xw
    element3 = np.dot(element1, w)

    # 2((X.T)Xw - (X.T)y)
    element4 = 2 * (element3 - element2)

    # compute the gradient as result
    result = np.divide(element4, X.shape[0])

    '''
    a = y - X * w
    double = -2 * X.T
    scale = double * a
    return scale / X.shape[0]
    '''
    return result


# A helper to compute wj
def formula_wj(X, y, i_in, K, j, w):

    batch_sampler = BatchSampler(X, y, j)

    g_set = []

    for i in range(K):
        X_b, y_b = batch_sampler.get_batch()
        batch_g = lin_reg_gradient(X_b, y_b, w)
        g_set.append(batch_g[i_in])

    n = len(g_set)

    # Compute gradients mean.
    ave_g = sum(g_set) / float(n)

    sum_up = []
    for item in g_set:
        sum_up.append((item - ave_g) ** 2)

    result = sum(sum_up) / (n - 1)

    return result


# A helper to draw q3.6 graph.
def visualize(X, y, K, w):

    temp = []
    for i in range(1, 401):
        temp.append(np.array(np.log(i)))

    plt.figure(figsize=(20, 5))
    feature_count = X.shape[1]

    # i: index
    for i in range(feature_count):
        plt.subplot(3, 5, i + 1)
        log = []

        for j in range(1, 401):
            log.append(np.log(formula_wj(X, y, i, K, j, w)))

        # Make a scatter plot of X[:, i] vs y. Marker size is scaled by s and marker color is mapped to c.
        plt.scatter(temp, log, s=35, c="c", marker=".", alpha=.5)

        # Set the label of x axis.
        plt.xlabel("Index")

        # Set the label of y axis.
        plt.ylabel("Log: {}".format(i+1))

    plt.tight_layout()
    plt.show()


def main():
    # Load data and randomly initialise weights
    X, y, w = load_data_and_init_params()
    # Create a batch sampler to generate random batches from data
    batch_sampler = BatchSampler(X, y, BATCHES)

    # Example usage
    # X_b, y_b = batch_sampler.get_batch()
    # batch_grad = lin_reg_gradient(X_b, y_b, w)

    # by assignment handout q3.5.
    K = 500
    m = 50

    # Compute the actual gradient g.
    g = lin_reg_gradient(X, y, w)

    # Loop 500 time as assignment requirements to sum up all gradients in order to get gradients mean below.
    total = 0
    for i in range(K):
        X_b, y_b = batch_sampler.get_batch(m=m)
        total += lin_reg_gradient(X_b, y_b, w)

    # Compute gradients mean.
    ave_g = np.divide(total, K)

    # Subtract arguments to get the difference between mean and actual values, element-wise.
    dif_array = np.subtract(ave_g, g)

    # Return the element-wise square of these differences.
    squ = np.square(dif_array)

    # Sum of elements in square as Squared Distance. Return as an scalar.
    squ_dis = np.sum(squ)

    # Compute the cosine similarity (cos theta) between gradient and average of gradients.
    cos = cosine_similarity(ave_g, g)

    # Compute accuracy, not in requirements
    squ_root = np.sqrt(squ_dis)
    acc = np.divide(squ_root, g)

    # print result
    print("Squared distance: {}".format(squ_dis))
    print("Cosine similarity: {}".format(cos))
    print("Accuracy: {}".format(acc))

    print("Reminder: It will take more time (about 2-3 mins) to visualize problem q3.6. \n If you do not want to wait, "
          + "please stop running or commet line 218 in q3.py. \n "
          + "I have already printed enough imformation for problems before q3.6.")

    visualize(X, y, K, w)

if __name__ == '__main__':
    main()
