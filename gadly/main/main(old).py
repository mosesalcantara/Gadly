# Prerequisites
# pip install nltk
# pip install pattern

# import nltk
# nltk.download('averaged_perceptron_tagger')
# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('wordnet')
# nltk.download('omw-1.4')

import nltk
import random

from nltk.tokenize import word_tokenize, TreebankWordDetokenizer
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer
from pattern.en import pluralize, singularize

from .models import Data_set
class ML():

    def __init__(self):
        self.classifier = self.train()

    def gen_sen_features(self, word):
        features = {}
        sensitive = ['man', 'woman', 'men', 'women', 'boy', 'girl', 'lady', 'ess', 'her',
                     'brother', 'sister', 'father', 'mother', 'female', 'male', 'daughter', 'son',
                     'husband', 'wife', 'queen', 'king']

        for sen_word in sensitive:
            features["has({})".format(sen_word)] = (sen_word in word.lower())
        return features

    def train(self):
        gen_sen = []
        not_gen_sen = []
        
        gen_sen_q = Data_set.objects.filter(sen='sensitive').values()
        for row in gen_sen_q:
            gen_sen.append(row['word'])
        not_gen_sen_q = Data_set.objects.filter(sen='not_sensitive').values()
        for row in not_gen_sen_q:
            not_gen_sen.append(row['word'])

        labeled_words = ([(word, 'gen_sen') for word in gen_sen] +
                         [(word, 'not_gen_sen') for word in not_gen_sen])

        random.shuffle(labeled_words)

        featuresets = [(self.gen_sen_features(word), sensitivity)
                       for (word, sensitivity) in labeled_words]
        train_set, test_set = featuresets[1000:], featuresets[:1000]

        classifier = nltk.NaiveBayesClassifier.train(train_set)
        # print(nltk.classify.accuracy(classifier, test_set))
        # classifier.show_most_informative_features(5)
        return classifier

    def classify(self, word):
        result = self.classifier.classify(self.gen_sen_features(word))
        return result


class Main():

    def filter_words(self, txt):
        words_dict = {}
        count = 0
        ml = ML()
        words = word_tokenize(txt)

        for word in words:
            if word.casefold() not in set(stopwords.words("english")) and ml.classify(word) == 'gen_sen':
                words_dict[count] = {word: []}
                count += 1
        # for wordd in words_dict:
        #     if self.get_synonyms(wordd, pref)
        # print(f"Filtered Words: {words_dict}")
        return words_dict, words

    def get_synonyms(self, word, pref):
        syns = []
        ml = ML()

        for wn in wordnet.synsets(word):
            for syn in wn.lemmas():
                if (ml.classify(syn.name()) == 'not_gen_sen'):
                    if self.is_plural(word):
                        syns.append(pluralize(syn.name()))
                    elif not self.is_plural(word):
                        syns.append(syn.name())

        for det, rep in pref.items():
            if rep in syns:
                syns.insert(0, rep)
        syns = list(dict.fromkeys(syns))
        # print(f"Synonyms: {syns}")
        return syns

    def is_plural(self, word):
        wnl = WordNetLemmatizer()
        lemma = wnl.lemmatize(word, 'n')
        return True if word is not lemma else False

    def filter_synonyms(self, words_dict, pref):
        rem_list=[]
        for ind, ent in words_dict.items():
            for det, rep in ent.items():
                words_dict[ind][det] = self.get_synonyms(det, pref)
                if len(words_dict[ind][det]) == 0:
                    rem_list.append(ind)
                    
        for ind in rem_list:
            del words_dict[ind]

        # print(f"Words Dictionary: {words_dict}")
        return words_dict

    def replace_words(self, words, words_dict):
        for ind, ent in words_dict.items():
            for det, rep in ent.items():
                if rep != []:
                    words = list(map(lambda x: x.replace(det, rep[0]), words))
        sen = TreebankWordDetokenizer().detokenize(words)
        return words, sen

    def main(self, txt, pref={}):
        words_dict = {}
        words_data = {'dets': [], 'reps': [], 'syns': [], 'rep_dict': {}}
        
        words_dict, words = self.filter_words(txt)
        words_dict = self.filter_synonyms(words_dict, pref)
        words, sen = self.replace_words(words, words_dict)
       
        for ind, ent in words_dict.items():
            for det, rep in ent.items():
                words_data['dets'].append(det)
                words_data['reps'].append(rep[0])
                words_data['syns'].append(rep)
                words_data['rep_dict'][det] = rep[0]
                
        # print(words_data)
        return words_dict, words_data, words, sen

# obj = Main()
# words_dict, words_data, words, sen = obj.main('the chairman is also a fine firemen along with a mailman', pref={})
# print(f'Words Dictionary: {words_dict}')
# print(f'Data: {words_data}')
# print(f'Words: {words}')
# print(f'Sentence: {sen}')
