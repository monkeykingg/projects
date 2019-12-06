from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.tree import DecisionTreeClassifier, export_graphviz
import numpy as np
import random
import math


def load_data():
    # open data
    real_data = open("clean_real.txt", "r")
    fake_data = open("clean_fake.txt", "r")

    # to store all news headlines and count the total titles number
    total_data = []
    total_num = 0
    total_data_with_splited_words = []

    # to mark if the headline is real or fake
    marker = []

    # read all data line by line, create two store lists and one label list for them
    # total_data looks like this: ["this is an example", "too many headlines"]
    # total_data is for vectorizer
    # total_data_with_splited_words looks like this: [["this", "is", "an", "example"], ["too", "many", "headlines"]]
    # total_data_with_splited_words is for Q2 (d) to calculate information gain
    # the list marker is to to label if the headline is real or fake
    for line in real_data:
        total_data.append(line.strip())
        total_num += 1
        marker.append(1)
        total_data_with_splited_words.append(line.split())

    for line in fake_data:
        total_data.append(line.strip())
        total_num += 1
        marker.append(0)
        total_data_with_splited_words.append(line.split())

    real_data.close()
    fake_data.close()

    # by handout, we use 70% data for training, 15% data for validation, and 15% data for testing
    total_training_bound = math.floor(0.7 * total_num)
    total_validation_bound = math.floor(0.85 * total_num)

    # randomize all news headlines and all markers with the same order,
    # to make sure we can still determine the title is real or fake even after randomization
    random_number = random.randint(1, 1000)
    random.Random(random_number).shuffle(total_data)
    random.Random(random_number).shuffle(marker)
    random.Random(random_number).shuffle(total_data_with_splited_words)

    # generate a training set without vectorized,
    # example: (if training set is 50% of full data)
    # total_data_with_splited_words = [["this", "is", "an", "example"], ["too", "many", "headlines"]]
    # training_set_without_vectorized = [["this", "is", "an", "example"]]
    training_set_without_vectorized = total_data_with_splited_words[:total_training_bound]

    # some common steps of vectorizer from the documents given by a1 handout
    vec_cv = CountVectorizer()
    total_vectorizer = vec_cv.fit_transform(total_data)

    # get all feature names (i.e. the vocabulary) of all headlines for future use
    vocabulary = vec_cv.get_feature_names()

    total_vectorizer.toarray()

    # divide data into three sets
    training = total_vectorizer[:total_training_bound]
    validation = total_vectorizer[total_training_bound:total_validation_bound]
    test = total_vectorizer[total_validation_bound:]

    # as well as the maker
    training_marker = marker[:total_training_bound]
    validation_marker = marker[total_training_bound:total_validation_bound]
    test_marker = marker[total_validation_bound:]

    return training, training_marker, validation, validation_marker, test, test_marker, vocabulary, \
           training_set_without_vectorized, total_data_with_splited_words, marker


def select_model():
    # load data
    training, training_marker, validation, validation_marker, test, test_marker, vocabulary, \
    training_set_without_vectorized, total_data_with_splited_words, marker = load_data()

    # fake = 0, real = 1
    classifiers = ["fake", "real"]

    # by handout, we should select five different depths
    depths = [3, 10, 20, 50, 100]
    # as well as two different criteria
    split_criterias = ["gini", "entropy"]

    # init some variables first for future replacement
    scores = []
    best_depth = 0
    best_criteria = ""

    # loop over all combinations to find the best one
    for depth in depths:
        for criteria in split_criterias:

            temp_dtc = DecisionTreeClassifier(max_depth=depth, criterion=criteria)
            temp_dtc.fit(training, training_marker)

            # using predict instead of directly using score, hinted by the instructor on piazza
            temp_marker = temp_dtc.predict(validation)
            error = np.sum(validation_marker != temp_marker)

            # score means the accuracy, the higher, the better
            score = (len(validation_marker) - error) / len(validation_marker)
            scores.append(score)

            print("Depth: ", depth, " Criteria: ", criteria, " Accuracy: ", score)

            # if the score is the best, update depth and criteria
            if score >= max(scores):
                best_depth = depth
                best_criteria = criteria

    # build the test decision tree by using the best results
    test_tree = DecisionTreeClassifier(max_depth=best_depth, criterion=best_criteria)
    test_tree.fit(training, training_marker)
    final_score = max(scores)
    print("\nBest accuracy: ", final_score)
    print("Best depth from [3, 10, 20, 50, 100]: ", best_depth)
    print("Best criteria from ['gini', 'entropy']: ", best_criteria)

    # visualize the graph as a display text
    export_graphviz(test_tree,
                    out_file="./test_tree.dot",
                    max_depth=2,
                    feature_names=vocabulary,
                    class_names=classifiers,
                    rounded=True,
                    filled=True,
                    special_characters=True)

    return test_tree, best_depth, best_criteria


# helper function for information gain calculation
def log(x):
    if x != 0:
        return math.log(x, 2)
    else:
        return 0


# helper function that using code to achieve the formula from slides
def IG_computor(root_fake, root_real, left_fake, left_real, right_fake, right_real):
    root_total = root_fake + root_real
    left_total = left_fake + left_real
    right_total = right_fake + right_real

    p_root_real = root_real / root_total
    p_root_fake = root_fake / root_total
    p_left_real = left_real / left_total
    p_left_fake = left_fake / left_total
    p_right_real = right_real / right_total
    p_right_fake = right_fake / right_total

    H_y = -(p_root_real * log(p_root_real) + p_root_fake * log(p_root_fake))
    H_yx1 = -p_left_real * log(p_left_real) - p_left_fake * log(p_left_fake)
    H_yx2 = -p_right_real * log(p_right_real) - p_right_fake * log(p_right_fake)

    print("H(y) = ", H_y, " H(y|x1) = ", H_yx1, " H(y|x2) = ", H_yx2)

    IG_yx = H_y - H_yx1 * (left_total / root_total) - H_yx2 * (right_total / root_total)

    print("IG(y|x) = ", IG_yx)

    return IG_yx


# you don't have to input training set. Any data set with splitted words & corresponding labels are OK,
# make sure the input data set is not vectorized
def compute_information_gain(data_set, marker, keyword):
    total_num_of_data = len(marker)

    # within means the headline contains the keyword
    root_within = []
    root_within_marker = []
    root_without = []
    root_without_marker = []

    # init counters, within goes left, without goes right
    root_fake = 0
    root_real = 0
    left_fake = 0
    left_real = 0
    right_fake = 0
    right_real = 0

    # loop over all headlines in training_set_without_vectorized,
    # find the headlines that contain the keyword,
    # save them as well as their labels
    for headline_index in range(total_num_of_data):
        if keyword in data_set[headline_index]:
            root_within.append(data_set[headline_index])
            root_within_marker.append(marker[headline_index])
        else:
            root_without.append(data_set[headline_index])
            root_without_marker.append(marker[headline_index])

    # count the number of real headlines and fake headlines
    for headline_index in range(total_num_of_data):
        if marker[headline_index] == 1:
            root_real += 1
        else:
            root_fake += 1

    for headline_index in range(len(root_within)):
        if root_within_marker[headline_index] == 1:
            left_real += 1
        else:
            left_fake += 1

    for headline_index in range(len(root_without)):
        if root_without_marker[headline_index] == 1:
            right_real += 1
        else:
            right_fake += 1

    # compute information gain
    IG_yx = IG_computor(root_fake, root_real, left_fake, left_real, right_fake, right_real)

    return IG_yx


if __name__ == '__main__':
    training, training_marker, validation, validation_marker, test, test_marker, vocabulary, \
    training_set_without_vectorized, total_data_with_splited_words, marker = load_data()

    select_model()

    print("\nTopmost split IG of handout tree data: ")
    IG_computor(1101, 1778, 890, 1778, 211, 0)

    print("\nTopmost split IG of Q2.(c): ")
    IG_computor(930, 1356, 673, 1255, 257, 101)

    print("=====================================================================================")

    keyword = "trump"
    print(
        "\nCompute the information gain by input total data without vectorized (if you want, "
        "you can use different data set, as long as they are not vectorized), "
        "the labels corresponding to the data,  and the keyword:", keyword)
    compute_information_gain(total_data_with_splited_words, marker, keyword)

    print(
        "\nCompute the information gain by input training data without vectorized (if you want, "
        "you can use different data set, as long as they are not vectorized), "
        "the labels corresponding to the data,  and the keyword:", keyword)
    compute_information_gain(training_set_without_vectorized, training_marker, keyword)

    print("=====================================================================================")

    keyword = "donald"
    print(
        "\nCompute the information gain by input total data without vectorized (if you want, "
        "you can use different data set, as long as they are not vectorized), "
        "the labels corresponding to the data,  and the keyword:", keyword)
    compute_information_gain(total_data_with_splited_words, marker, keyword)

    print(
        "\nCompute the information gain by input training data without vectorized (if you want, "
        "you can use different data set, as long as they are not vectorized), "
        "the labels corresponding to the data,  and the keyword:", keyword)
    compute_information_gain(training_set_without_vectorized, training_marker, keyword)

    print("=====================================================================================")

    keyword = "hillary"
    print(
        "\nCompute the information gain by input total data without vectorized (if you want, "
        "you can use different data set, as long as they are not vectorized), "
        "the labels corresponding to the data,  and the keyword:", keyword)
    compute_information_gain(total_data_with_splited_words, marker, keyword)

    print(
        "\nCompute the information gain by input training data without vectorized (if you want, "
        "you can use different data set, as long as they are not vectorized), "
        "the labels corresponding to the data,  and the keyword:", keyword)
    compute_information_gain(training_set_without_vectorized, training_marker, keyword)
