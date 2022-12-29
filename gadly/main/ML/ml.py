import nltk 
import random

class ML():
    
    def __init__(self):
        self.classifier = self.train()
        
    def gen_sen_features(self, word):
        features = {}
        sensitive = ["man", "woman", 'men', 'women', 'boy', 'girl', 'lady', 'ess', 'her']
        
        for sen_word in sensitive:
            features["has({})".format(sen_word)] = (sen_word in word.lower())
        return features

        # print(gen_sen_features('Chairman'))

    def train(self):
        gen_sen = []
        not_gen_sen = []
        
        f = open(r'C:\Users\Chester Martinez\OneDrive\Documents\School\App Dev\CapstoneProj\gadly\main\ML\gen_sen.txt', 'r')
        for line in f:
            gen_sen.append(line.strip())
        f.close()
        
        f = open(r'C:\Users\Chester Martinez\OneDrive\Documents\School\App Dev\CapstoneProj\gadly\main\ML\not_gen_sen.txt', 'r')
        for line in f:
            not_gen_sen.append(line.strip())
        f.close()

        labeled_words = ([(word, 'gen_sen') for word in gen_sen] +
                        [(word, 'not_gen_sen') for word in not_gen_sen])

        random.shuffle(labeled_words)

        featuresets = [(self.gen_sen_features(word), sensitivity) for (word, sensitivity) in labeled_words]
        train_set, test_set = featuresets[1000:], featuresets[:1000]

        classifier = nltk.NaiveBayesClassifier.train(train_set) 
        return classifier

    def classify(self, word):
        result = self.classifier.classify(self.gen_sen_features(word))
        return result
    