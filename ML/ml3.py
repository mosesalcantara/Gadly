import nltk 
import random

gen_sen = []
not_gen_sen = []

def gen_sen_features(word):
    features = {}
    sensitive = ["man", "woman", 'boy', 'girl', 'lady', 'ess', 'her']
    
    for sen_word in sensitive:
        features["has({})".format(sen_word)] = (sen_word in word.lower())
    return features

# print(gen_sen_features('Chairman'))

f = open('gen_sen.txt', 'r')
for line in f:
    gen_sen.append(line.strip())
f.close()

f = open('not_gen_sen.txt', 'r')
for line in f:
    not_gen_sen.append(line.strip())
f.close()

labeled_words = ([(word, 'gen_sen') for word in gen_sen] +
                 [(word, 'not_gen_sen') for word in not_gen_sen])

# print(labeled_words)

random.shuffle(labeled_words)
# print(labeled_words)

featuresets = [(gen_sen_features(word), sensitivity) for (word, sensitivity) in labeled_words]
train_set, test_set = featuresets[1000:], featuresets[:1000]

# print(featuresets)
# print(train_set)
# print(test_set)

classifier = nltk.NaiveBayesClassifier.train(train_set)

# print(classifier.classify(gen_sen_features('humankind')))

print(nltk.classify.accuracy(classifier, test_set))
classifier.show_most_informative_features(5)