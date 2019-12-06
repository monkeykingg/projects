import numpy as np


def huber_gradient(delta, y):
    # formula from q1 (a) and (b)
    first_array_index = np.where(np.absolute(y) <= delta)
    second_array_index = np.where(np.absolute(y) > delta)

    # we need to record the loss and the gradient but we do not want to change the original y
    loss_gradient = np.copy(y)

    # formula from q1 (a) and (b)
    loss_gradient[first_array_index] = y[first_array_index]
    loss_gradient[second_array_index] = delta * y[second_array_index] / np.absolute(y[second_array_index])

    return loss_gradient


# design matrix X, target vector y
def huber_gradient_descent(X, y, delta):
    data_num = X.shape[0]
    precision = 0.00001
    max_iters = 10000
    iters = 0  # iteration counter

    # init w and b to all zeros
    w = np.zeros(len(X[0]))
    b = 0

    while iters < max_iters:
        trans_X = np.transpose(X)
        new_y = np.dot(X, w) + b
        input_y = new_y - y

        loss_gradient = huber_gradient(delta, input_y)

        # update w and b
        Lw = np.dot(trans_X, loss_gradient) / data_num
        Lb = np.sum(loss_gradient) / data_num
        w = w - (precision * Lw)
        b = b - (precision * Lb)

        iters = iters + 1

    return w, b
