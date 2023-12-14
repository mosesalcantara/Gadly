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
import pandas as pd
import numpy as np
import spacy
import json
import torch
import random
import re

from nltk.tokenize import word_tokenize, TreebankWordDetokenizer
from nltk.corpus import stopwords, wordnet, words
from nltk.stem import WordNetLemmatizer
from nltk.tag import pos_tag
from pattern.en import pluralize, singularize

from transformers import PegasusForConditionalGeneration, PegasusTokenizerFast
from sklearn.feature_extraction import DictVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from gensim.models import KeyedVectors
from joblib import dump, load

# from .models import Word, Synonyms, Synset


class ML():
    def __init__(self):
        f = open(r'/home/dev/gadly/gadly/backend/ML/backend/compound_words.json')
        self.compound_words = json.load(f)
        self.nlp = spacy.load('en_core_web_sm')
        
        try: 
            self.model = load(r'/home/dev/gadly/gadly/backend/ML/joblib/model.joblib')
            self.vectorizer = load(r'/home/dev/gadly/gadly/backend/ML/joblib/vectorizer.joblib')
            self.classifier = load(r'/home/dev/gadly/gadly/backend/ML/joblib/classifier.joblib')
            self.classifier_w2v = load(r'/home/dev/gadly/gadly/backend/ML/joblib/classifier_w2v.joblib')
        except FileNotFoundError:
            self.model, self.vectorizer, self.classifier, self.classifier_w2v = self.train() 
    
    
    def train(self):    
        model = KeyedVectors.load_word2vec_format(
            r'/home/dev/gadly/gadly/backend/ML/backend/GoogleNews-vectors-negative300.bin',
            binary = True, limit = 100000
        )
        
        dataset_path = open(r'/home/dev/gadly/gadly/backend/ML/backend/backend_dataset.json')
        backend_dataset = json.load(dataset_path)
        
        dataset_sen= list(set(backend_dataset['male'] + backend_dataset['female']))
        dataset_neu = list(set(backend_dataset['neutral']))
        num_dataset = 900
        random.shuffle(dataset_sen)
        dataset_sen = dataset_sen[:num_dataset]
        random.shuffle(dataset_neu)
        dataset_neu = dataset_neu[:num_dataset]
        
        dataset = {'word': [], 'gender': []}
        for data in dataset_sen:
            dataset['word'].append(data)
            dataset['gender'].append(1)
        for data in dataset_neu:
            dataset['word'].append(data)
            dataset['gender'].append(0)

        labels = []
        features = []
        gender_sen = []
        gender_neu = []
        labels_w2v = []

        for word, gender in zip(dataset['word'], dataset['gender']):
            word = self.nlp(word)[0].lemma_
            try:
                split_word = self.compound_words[word]
            except KeyError:
                split_word = re.split('_|-', word)

            word_feat = {'word': split_word, 'word_length': len(word), 'prefix': [word[:4],word[:3], word[:2]], 'suffix': [word[-4:], word[-3:], word[-2:]]}
            features.append(word_feat)
            labels.append(gender)

            if word in model:
                if gender == 1:
                    gender_sen.append(model[word])
                else:
                    gender_neu.append(model[word])
                labels_w2v.append(gender)
        
        vectorizer = DictVectorizer(sparse=False)
        features = vectorizer.fit_transform(features)
        x_train, x_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)

        classifier = LogisticRegression()
        classifier.fit(x_train, y_train)
        print(f"{classifier.score(x_test, y_test)}")

        final_dataset = gender_sen + gender_neu
        classifier_w2v = LogisticRegression(max_iter= 10000)
        classifier_w2v.fit(final_dataset, labels_w2v)
        x_train_w2v, x_test_w2v, y_train_w2v, y_test_w2v = train_test_split(final_dataset, labels_w2v, test_size=0.2, random_state=42)
        print(f"{classifier_w2v.score(x_test_w2v, y_test_w2v)}")
        
        dump(model, r'/home/dev/gadly/gadly/backend/ML/joblib/model.joblib')
        dump(vectorizer, r'/home/dev/gadly/gadly/backend/ML/joblib/vectorizer.joblib')
        dump(classifier, r'/home/dev/gadly/gadly/backend/ML/joblib/classifier.joblib')
        dump(classifier_w2v, r'/home/dev/gadly/gadly/backend/ML/joblib/classifier_w2v.joblib')
        return model, vectorizer, classifier, classifier_w2v
    
    
    def classify(self,word):
        word = self.nlp(word)[0].lemma_
        try:
            split_word = self.compound_words[word]
        except KeyError:
            split_word = re.split('_|-', word)

        word_feat = {'word': split_word, 'word_length': len(word), 'prefix': [word[:4],word[:3], word[:2]], 'suffix': [word[-4:], word[-3:], word[-2:]]} 
        word_feat = self.vectorizer.transform([word_feat])
        pred = self.classifier.predict(word_feat)[0]
        return pred
        
        
class Para_txt():
    def __init__(self):
        self.nlp = spacy.load('en_core_web_sm')
    
        
    def filter_words(self, txt):
        words = []
        nostop = []
        nouns = []
        words_list = []
        ml = ML()
        
        words = word_tokenize(txt)
        doc = self.nlp(txt)
                
        for word in words:
            if word.lower() not in set(stopwords.words("english")):
                nostop.append(word)        
        
        for token in doc:
            if (token.pos_ == 'NOUN' or token.pos_ == 'PROPN') and not any(token.i >= ent.start and token.i < ent.end for ent in doc.ents):
                nouns.append(token.text)
                
        for word in nouns:
            if ml.classify(word) == 1:
                words_list.append({word:[]})
        return words_list, words

    def is_plural(self, word):
        wnl = WordNetLemmatizer()
        lemma = wnl.lemmatize(word, 'n')
        return True if word is not lemma else False
    

    def get_synonyms(self, word, tokenized_sent, pref):
        syns = []
        ml = ML()
        
        lemma_word = self.nlp(word)[0].lemma_
        synsent = lesk(context_sentence=tokenized_sent, ambiguous_word=lemma_word, pos = 'n')
        
        for syn in synsent.lemmas():
            if (ml.classify(syn.name()) == 0):  
                if self.is_plural(word):
                    syns.append(pluralize(syn.name()))
                elif not self.is_plural(word):  
                    syns.append(syn.name())   
                        
        for det, rep in pref.items():
            if rep in syns:
                syns.insert(0, rep)
        syns = list(dict.fromkeys(syns))
        return syns


    def filter_synonyms(self, words_list, pref):
        rem_list=[]
        
        for ind, ent in enumerate(words_list):
            for det, reps in ent.items():
                words_list[ind][det] = self.get_synonyms(det, pref)
                
                if not words_list[ind][det]:
                    rem_list.append(det)
        
        for name in rem_list:
            words_list = self.remove_dict(words_list, name)

        return words_list
    
    
    def remove_dict(self, words_list, name):
        return [word for word in words_list if list(word.keys())[0] != name]


    def replace_words(self, words, words_list):
        for ent in words_list:
            for det, reps in ent.items():
                if reps != []:
                    words = list(map(lambda x: x.replace(det, reps[0]), words))
        sen = TreebankWordDetokenizer().detokenize(words)
        return words, sen
    
    
    def para_txt(self, sent, pref={}):
        words_list = [] 
        words_data = {'dets': [], 'reps': [], 'syns': [], 'rep_dict': {}}        
        
        words_list, words = self.filter_words(sent)
        words_list = self.filter_synonyms(words_list, pref)
        words, sen = self.replace_words(words, words_list)

        for ent in words_list:
            for det, reps in ent.items():
                words_data['dets'].append(det)
                words_data['reps'].append(reps[0])
                words_data['syns'].append(reps)
                words_data['rep_dict'][det] = reps[0]
        return words_list, words_data, words, sen


# para = Para_txt()
# words_list, words_data, words, sen = para.para_txt('the chairman fireman', pref={})
# print(f'Words List: {words_list}')
# print(f'Data: {words_data}')
# print(f'Words: {words}')
# print(f'Sentence: {sen}')