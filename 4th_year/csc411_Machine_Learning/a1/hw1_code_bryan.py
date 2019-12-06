from sklearn.tree import DecisionTreeClassifier, export_graphviz
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
import numpy as np


def load_data(fake="./clean_fake.txt", real="./clean_real.txt"):
    """
    Loads the data from file 'clean_fake.txt' and 'clean_real.txt',
    preprocesses it using a vectorizer,
    and splits the entire dataset randomly into 70% training,
    15% validation, and 15% test examples.
    """

    # First, we read in the files.
    with open(fake, 'r') as f1:
        fake = f1.readlines()

    with open(real, 'r') as f2:
        real = f2.readlines()

    # split each headline in fake.
    # for i in range(len(fake)):
    #     fake[i] = fake[i].split()

    # split each headline in real.
    # for j in range(len(real)):
    #     real[j] = real[j].split()

    # Concatenate fake_headlines and real_headlines into one list.
    news_headlines = fake + real

    # Preprocesses the data using a vectorizer.
    vectorizer = CountVectorizer()
    data = vectorizer.fit_transform(news_headlines)

    # Make a corresponding label list, 0 for fake news, 1 for real news.
    labels = [0 for x in range(len(fake))] + [1 for y in range(len(real))]
    labels = np.asarray(labels)

    # Splits the dataset randomly into 70% training set, and 30% remaining to be further split.
    headlines_train, headlines_rem, labels_train, labels_rem \
        = train_test_split(data, labels, test_size=0.3)

    # Splits the remaining dataset into 15% validation and 15% testing set.
    headlines_vali, headlines_test, labels_vali, labels_test \
        = train_test_split(headlines_rem, labels_rem, test_size=0.3)

    return headlines_train, labels_train, headlines_vali, labels_vali, \
           headlines_test, labels_test, news_headlines


def select_model(maxDepth, splitCriterion):
    """
    splitCriterion: The function to measure the quality of a split.
    Supported criteria are "gini" for the Gini impurity, "entropy" for the information gain.

    Trains the decision tree classifier by specifying different
    values of max_depth, as well as different split criteria
    (information gain and Gini coefficient).
    """

    headlines_train, labels_train, headlines_vali, labels_vali, headlines_test, labels_test, news_headlines \
        = load_data()

    # the decision tree classifier.
    mytree = DecisionTreeClassifier(max_depth=maxDepth, criterion=splitCriterion)
    mytree.fit(headlines_train, labels_train)

    # Evaluates the performance of the model on the validation set.
    # Print the resulting accuracy of our DecisionTree model.
    print("Given max_depth:", maxDepth, ", and splitCriterion:", splitCriterion,
          ", the resulting accuracy of our DecisionTree model is:",
          mytree.score(headlines_vali, labels_vali), "\n")


    # Next,
    # Use the hyperparameters which achieved the highest validation
    # accuracy to fit a model, then evaluate it by test set.
    tree_test = DecisionTreeClassifier(max_depth=5, criterion="entropy")
    tree_test.fit(headlines_train, labels_train)
    print(mytree.score(headlines_test, labels_test))

    export_graphviz(tree_test,
                    out_file="./mytree.dot",
                    rounded=True,
                    filled=True)


def compute_information_gain():
    """Computes the information gain of a split on the training data.
    """
    return


if __name__ == '__main__':
    # select_model(5, "gini")
    # select_model(10, "gini")
    # select_model(15, "gini")
    # select_model(20, "gini")
    # select_model(25, "gini")

    # select_model(5, "entropy")
    # select_model(10, "entropy")
    select_model(15, "entropy")
    # select_model(20, "entropy")
    # select_model(25, "entropy")
