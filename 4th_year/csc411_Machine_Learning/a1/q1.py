from sklearn import datasets
import matplotlib.pyplot as plt
import numpy as np
import pandas as pad


def load_data():
    boston = datasets.load_boston()
    X = boston.data
    y = boston.target
    features = boston.feature_names
    return X,y,features


def visualize(X, y, features, coe):

    plt.figure(figsize=(20, 5))
    feature_count = X.shape[1]

    # i: index
    for i in range(feature_count):
        plt.subplot(3, 5, i + 1)
        #TODO: plot feature i against y

        # Make a scatter plot of X[:, i] vs y. Marker size is scaled by s and marker color is mapped to c.
        plt.scatter(X[:, i], y, s=35, c="c", marker=".", alpha=.5)

        # Set the label of x axis.
        plt.xlabel(features[i]+", Weight = "+str(coe[i]))

        # Set the label of y axis.
        plt.ylabel("Housing Price")

    plt.tight_layout()
    plt.show()


def fit_regression(X,y):
    #TODO: implement linear regression
    # Remember to use np.linalg.solve instead of inverting!
    # raise NotImplementedError()

    # add bias, a new column assume X are all 1
    # insert 1 at botton along every axis in X
    # X.shape[1] = 13, which is the indices before 1 is inserted
    X = np.insert(X, X.shape[1], 1, axis=1)

    # Formulas below are all according to lecture slides.

    # (The transpose of X dot product X) = a;
    # (The transpose of X dot product Y) = b.
    # a =(X^T)X, b = (X^T)y
    a = np.dot(X.T, X)
    b = np.dot(X.T, y)

    # there is no difference if you use np.linalg.inv. ex: inverse = np.linalg.inv(a)
    # the theorem is "w^* = (((X^T)X)^(-1)) * ((X^T)y)", simplify to "w^* = (a^(-1))b" or "a(w^*) = b" by matrix def
    # np.linalg.solve can return x in equation "ax = b" by inputting (a, b)
    # and in this part, the equation is "a(w^*) = b", so np.linalg.solve will return w^*
    # use coe to represent coefficient
    coe = np.linalg.solve(a, b)

    return coe


# A helper to divide data into training and test sets, where the training set consists of 80% of the data points.
# Chosen at random.
# Then return data sets for training and testting, with numpy style.
def divide_data(X, y, test_sets_size):

    # In order to chosen at random, use numpy.random.choice as A1 Hint, without replacement.
    # Put test_sets_size percentage(in q1, it should be 20%) data into "test_sets" for future test.
    test_sets = np.random.choice(len(X), int(len(X) * test_sets_size), replace=False)

    # for grouping sets by test, train, X and y.
    test_X = []
    test_y = []
    train_X = []
    train_y = []

    # loop over X and find out what data should be tested, what data should be trained.
    for i in range(len(X)):
        if i in test_sets:
            test_X.append(X[i])
            test_y.append(y[i])
        else:
            train_X.append(X[i])
            train_y.append(y[i])

    return np.array(test_X), np.array(test_y), np.array(train_X), np.array(train_y)


# A helper to get result of predicted fitted values
def predictor(X, coe):

    # like fit_regression
    # add bias, a new column assume X are all 1
    # insert 1 at botton along every axis in X
    # X.shape[1] = 13, which is the indices before 1 is inserted
    X = np.insert(X, X.shape[1], 1, axis=1)

    # Use the output coefficient of fit_regression
    # do dot product with X and coefficient
    # credit to lecture slides
    return np.dot(X, coe)


# A helper to normalize data
def normalize(X):
    mean = X - np.mean(X, axis=0, keepdims=True)
    std = np.std(X, axis=0, keepdims=True)
    normal = mean / std
    return normal


# Draw a weight graph for checking, no in requirements.
def weight_graph(w):

    i = range(len(w))

    plt.title("Weights on different features")
    plt.plot(i, w, linestyle='-', marker='.')

    plt.xlabel('Features', fontsize=10, color='blue')
    plt.ylabel('Weight', fontsize=10, color='blue')

    plt.grid(True)
    plt.show()
    print(w)


def main():
    # Load the data
    X, y, features = load_data()

    # Print data for checking and debugging
    print("-------------------------------------------------------------------------------")
    print("Total Data number: ", X.shape[0])
    print("Features number: ", X.shape[1])
    print("Features: {}".format(features))
    print("-------------------------------------------------------------------------------")

    X = normalize(X)

    # Print data for checking and debugging
    print("-------------------------------------------------------------------------------")
    print("Data: {}".format(X))
    print("-------------------------------------------------------------------------------")
    print("Features: ")
    print(pad.DataFrame(X).describe())
    print("-------------------------------------------------------------------------------")
    print("Targets: ")
    print(pad.DataFrame(y).describe())
    print("-------------------------------------------------------------------------------")

    #TODO: Split data into train and test

    test_sets_size = 0.2
    test_X, test_y, train_X, train_y = divide_data(X, y, test_sets_size)

    # check data in training X
    print("Data in training X: ")
    print(train_X)
    print("-------------------------------------------------------------------------------")

    # Fit regression model
    w = fit_regression(train_X, train_y)

    # check data in training X after apply fit_regression
    print("Data in training X after apply fit_regression: ")
    print(train_X)
    print("-------------------------------------------------------------------------------")

    # Visualize the features
    visualize(X, y, features, w)

    # Compute fitted values, MSE(Mean Square Error), etc.
    # Formulas below are all according to lecture slides.

    # Call helper to predict fitted values, in order to compare with real values.
    fitted_values = predictor(test_X, w)

    # "mean" function is able to get average
    # "test_y - fitted_values" can give us the gap between fitted_values and real values in test_y
    # "**2" aim to make all gaps to be positive
    train_mse = np.mean((test_y - fitted_values) ** 2)

    print("MSE(Mean Square Error): {}".format(train_mse))

    # Compute Root Mean Square Deviation
    rmsd = train_mse ** 0.5
    print("RMSD(Root Mean Square Deviation): {}".format(rmsd))

    # Compute Mean Absolute Percentage Error
    element = np.abs((test_y - fitted_values)/test_y)
    mean = np.mean(element)
    mape = 100 * mean
    print("MAPE(Mean Absolute Percentage Error): {}".format(mape))

    print("All results above are after normalizing. If you need results without normalization, please comment line 143 in q1.py.")

    # Draw a weight graph for checking, no in requirements.
    # weight_graph(w)


if __name__ == "__main__":
    main()

