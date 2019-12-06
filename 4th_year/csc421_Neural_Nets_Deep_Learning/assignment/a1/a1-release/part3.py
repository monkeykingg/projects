from language_model import *

model = train(16, 128)

#model.tsne_plot()

#find_occurrences("government", "of", "united")
#model.predict_next_word("government", "of", "united")

#find_occurrences("city", "of", "new")
#model.predict_next_word("city", "of", "new")

#find_occurrences("who", "is", "my")
#model.predict_next_word("who", "is", "my")

d1 = model.word_distance("new", "york")
print('')
print('Distance between new and york:')
print(d1)

d2 = model.word_distance("government", "political")
print('')
print('Distance between government and political:')
print(d2)

d3 = model.word_distance("government", "university")
print('')
print('Distance between government and university:')
print(d3)
