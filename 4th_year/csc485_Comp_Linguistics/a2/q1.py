import nltk
from nltk import CFG

# file location for all required files
grammar_fname = "q1.txt"
# single_sent_fname = "TEST CASES/single_sent.txt"

positive_fname = "q1_positive.txt"
negative_fname = "q1_negative.txt"

# # Print trees for one sentence
# file2 = open(grammar_fname,"r")

# grammar2 = CFG.fromstring(file2.read())

# with open(single_sent_fname) as f:
#     sent = f.readlines()

# sent_test_1 = [x.strip() for x in sent]

# parser2 = nltk.BottomUpChartParser(grammar2)

# for sent in sent_test_1:
#     for tree in parser2.parse(nltk.tokenize.word_tokenize(sent)):
#         print(tree)


print("======================== 3 ========================")

file1 = open(grammar_fname,"r")

grammar1 = CFG.fromstring(file1.read())

# TRUE CASE
positive_case = []
with open(positive_fname) as f:
    sent = f.readlines()
positive_case = [x.strip() for x in sent]

# FALSE CASE
negative_case = []
with open(negative_fname) as f:
    sent = f.readlines()
negative_case = [x.strip() for x in sent]

count = 0
parser1 = nltk.BottomUpChartParser(grammar1)

print("=====================True Cases=====================")
print("NOT PASS: ")
for sent_test in positive_case:
    i = 0
    for tree in parser1.parse(sent_test.split()):
            # print(tree)
        i += 1
    if i == 0:
        print(sent_test)
    else:
        count += 1

print("PASS: ", count)

print("=====================False Cases====================")

count = 0
print("NOT PASS: ")
for sent_test in negative_case:
    i = 0
    for tree in parser1.parse(sent_test.split()):
        # print(tree)
        i += 1
    if i > 0:
        print(sent_test)
    else:
        count +=1
print("PASS: ", count)


