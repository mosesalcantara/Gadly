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
import pandas as pd

from nltk.tokenize import word_tokenize, TreebankWordDetokenizer
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer
from nltk.tag import pos_tag
from pattern.en import pluralize, singularize

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

from .models import Dataset

from gensim.models import KeyedVectors
# model_path = '../GoogleNews-vectors-negative300.bin'
# model = KeyedVectors.load_word2vec_format(model_path, binary=True, limit = 500000)

class ML():
    def __init__(self):
        self.vectorizer = CountVectorizer()
        self.model = self.train()


    def train(self):
        dataset = Dataset.objects.all()
        # print(f"dataset:{dataset}")
        words = [data.word for data in dataset]
        labels = [data.sen for data in dataset]
        print(f"words:{words}")
        # print(f"labels{labels}")

        word_lengths = [len(word) for word in words]
        suffixes = [word[-3:] for word in words]
        prefixes = [word[:3] for word in words]
        features = [f"{word} {length} {suffix} {prefix}" for word, length, suffix, prefix in zip(words, word_lengths, suffixes, prefixes)]

        X = self.vectorizer.fit_transform(features)
        X_train, X_test, y_train, y_test = train_test_split(X, labels, test_size=0.2, random_state=42)

        model = LogisticRegression()
        model.fit(X_train, y_train)

        accuracy = model.score(X_test, y_test)
        print("Accuracy:", accuracy)

        return model

    def classify(self, word):
        # print((f"Word: {word}"))
        length = len(word)
        suffix = word[-3:]
        prefix = word[:3]
        feature = f"{word} {length} {suffix} {prefix}"

        X_new = self.vectorizer.transform([feature])
        # print(f"X_new: {X_new}")
        prediction = self.model.predict(X_new)[0]
        
        if prediction == 'sensitive':
            prediction = 'gen_sen'
            # similar_word = model.wv.most_similar(word)
            # print(similar_word)
        else:
            prediction = 'not_gen_sen'
        # print(f"Prediction: {prediction}")
        return prediction


class Para_txt():

    def filter_words(self, txt):
        nostop_words = []
        nouns = []
        words_dict = {}
        count = 0
        ml = ML()
        
        words = word_tokenize(txt)
        stop_words = set(stopwords.words("english"))
        
        for word in words:
            if word.lower() not in stop_words:
                nostop_words.append(word)        
        tagged_words = pos_tag(nostop_words)
        # print(tagged_words)
    
        for word,tag in tagged_words:
            if tag.startswith('NN') or tag == 'JJ':
                nouns.append(word)
        # print(f"Nonuns: {nouns}")
                
        for word in nouns:
            # if ml.classify(word) == 'gen_sen':
            # print(f"ML Classify: {ml.classify(word)}")
            
            if ml.classify(word) == 'gen_sen':
                # print(f"Wordnouns: {word}")
                # print(f"ML Classify: {ml.classify(word)}")

                words_dict[count] = {word: []}
                count += 1
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

    def para_txt(self, txt, pref={}):
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
