from sklearn.datasets import load_iris
from sklearn import tree
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.tree import DecisionTreeClassifier, export_graphviz
import random
import math

iris = load_iris()

a = ["a", 'b']

b = ["the apple", "it is bad"]

c = []

print(iris.feature_names)
print(iris.target_names)

print(np.array(a))

for line in b:
    c.append(line.split())

print(c)

def load_data():
    # open data
    real_data = open("clean_real.txt", "r")
    fake_data = open("clean_fake.txt", "r")

    # to store all news headlines and count the total titles number
    total_data = []
    total_num = 0

    # to mark if the headline is real or not
    marker = []

    for line in real_data:
        total_data.append(line.strip())
        total_num += 1
        marker.append(1)

    for line in fake_data:
        total_data.append(line.strip())
        total_num += 1
        marker.append(0)

    real_data.close()
    fake_data.close()

    total_training_bound = math.floor(0.7 * total_num)
    total_validation_bound = math.floor(0.85 * total_num)

    # randomize all news headlines and all markers with the same order,
    # to make sure we can still determine the title is real or not even after randomization
    random_number = random.randint(1, 1000)
    random.Random(random_number).shuffle(total_data)
    random.Random(random_number).shuffle(marker)

    # some common steps from the documents given by a1 handout
    vec_cv = CountVectorizer()
    total_vectorizer = vec_cv.fit_transform(total_data)

    # get all feature names (i.e. the vocabulary) of all headlines
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

    print(training)
    print(training_marker)
    print(total_num)

    return training, training_marker, validation, validation_marker, test, test_marker, vocabulary

load_data()



