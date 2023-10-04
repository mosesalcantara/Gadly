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
import numpy as np
import spacy
import json

from nltk.tokenize import word_tokenize, TreebankWordDetokenizer
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer
from nltk.tag import pos_tag
from pattern.en import pluralize, singularize

from transformers import GenerationMixin, TFGenerationMixin, PegasusForConditionalGeneration, PegasusTokenizerFast
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from gensim.models import KeyedVectors, Word2Vec
from joblib import dump, load

# from .models import Dataset
# from .utils import load_word2vec_model

class ML():
    def __init__(self):
        # model_path = r'C:\Users\Chester Martinez\OneDrive\Documents\School\App Dev\CapstoneProj\gadly\backend\ML\GoogleNews-vectors-negative300.bin'
        # self.word_vectors = KeyedVectors.load_word2vec_format(model_path, binary=True)
            
        try: 
            self.vectorizer = load(r'C:\Users\Chester Martinez\OneDrive\Documents\School\App Dev\CapstoneProj\gadly\backend\ML\joblib\vectorizer.joblib')
            self.classifier = load(r'C:\Users\Chester Martinez\OneDrive\Documents\School\App Dev\CapstoneProj\gadly\backend\ML\joblib\classifier.joblib')
        except FileNotFoundError:
            self.vectorizer, self.classifier = self.train() 
            
        # self.vectorizer, self.classifier = self.train() 
    
    
    def preprocess(self, text):
        words = text.split()
        stop_words = set(stopwords.words("english"))
        words = [word for word in words if word not in stop_words]
        
        words = pos_tag(words)
        words = [word for word, tag in words if tag.startswith('NN') or tag.startswith('JJ')]
        
        nlp = spacy.load('en_core_web_sm')
        doc = nlp(text)
        ents = [ent.text for ent in doc.ents]
        words = [word for word in words if word not in ents]
        
        text = " ".join(words)
        return text
    
    
    def train(self):
        f = open(r"C:\Users\Chester Martinez\OneDrive\Documents\School\App Dev\CapstoneProj\gadly\backend\ML\opensubtitles_inferred\opensubtitles_inferred.json")
        os_ds = json.load(f)
        
        train_os_ds = os_ds['train'] 
        test_os_ds = os_ds['test']
        val_os_ds = os_ds['validation']
        
        os_texts = train_os_ds['text']
        os_texts.extend(test_os_ds['text'])
        os_texts.extend(val_os_ds['text'])
        
        os_labels = train_os_ds['label']
        os_labels.extend(test_os_ds['label'])
        os_labels.extend(val_os_ds['label'])
        
        texts = os_texts
        init_labels = os_labels
        
        labels = []
        for label in init_labels:
            if label == 1 or label == 0:
                labels.append(1)
            else:
                labels.append(0)

        vectorizer = TfidfVectorizer(preprocessor=self.preprocess, use_idf= True)
        x = vectorizer.fit_transform(texts)
        
        classifier = LogisticRegression(max_iter= 10000)
        classifier.fit(x,labels)
        x_train, x_test, y_train , y_test = train_test_split(x, labels, test_size=0.2, random_state=42)
        print(f"{classifier.score(x_test, y_test)*100=}")

        dump(vectorizer, r'C:\Users\Chester Martinez\OneDrive\Documents\School\App Dev\CapstoneProj\gadly\backend\ML\joblib\vectorizer.joblib')
        dump(classifier, r'C:\Users\Chester Martinez\OneDrive\Documents\School\App Dev\CapstoneProj\gadly\backend\ML\joblib\classifier.joblib') 
        return vectorizer, classifier
    
    
    def classify(self, text):
        sen_words = []
        coefs = self.classifier.coef_[0]
        feat_names = self.vectorizer.get_feature_names_out()
        coefs_feat_names = sorted(zip(coefs, feat_names), reverse=True)
        
        ret_vec = TfidfVectorizer(preprocessor=self.preprocess, use_idf= True)
        ret_matrix = ret_vec.fit_transform([text])
        # print(ret_vec.vocabulary_)
        # print(ret_vec.get_feature_names_out())
        
        for ret_feat_name in ret_vec.get_feature_names_out():
            for coef, feat_name in coefs_feat_names:
                if ret_feat_name == feat_name and coef >= 0.5:
                    sen_words.append(ret_feat_name)
        
        matrix = self.vectorizer.transform([text])
        pred = self.classifier.predict(matrix)
        if pred == 1:
            pred = 'gender_sensitive'
        else:
            pred = 'gender_neutral'
            
        prob = self.classifier.predict_proba(matrix)[0]
        inst_prob = prob
        max_prob = max(inst_prob)
        confidence = max_prob / sum(inst_prob)
        print('Confidence: ', confidence)
        return pred, sen_words
    

class Para_txt():
    def filter_words(self, txt):
        words_list = []
        ml = ML()
         
        words = word_tokenize(txt)
        pred, sen_words = ml.classify(txt)
        for word in sen_words:
            words_list.append({word:[]})
        return words_list, words


    def is_plural(self, word):
        wnl = WordNetLemmatizer()
        lemma = wnl.lemmatize(word, 'n')
        return True if word is not lemma else False
    
    
    def get_synonyms(self, word, pref):
        syns = []
        ml = ML()

        for wn in wordnet.synsets(word):
            for syn in wn.lemmas():
                pred, sen_words = ml.classify(syn.name())
                if (pred == 'gender_neutral'):
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


    def filter_synonyms(self, words_list, pref):
        rem_list=[]
        # print(f"word list: {words_list}")
        
        for ind, ent in enumerate(words_list):
            for det, reps in ent.items():
                words_list[ind][det] = self.get_synonyms(det, pref)
                if len(words_list[ind][det]) == 0:
                    rem_list.append(ind)
            
        for ind in rem_list:
            del words_list[ind]
        # print(f"Words Dictionary: {words_dict}")
        return words_list


    def replace_words(self, words, words_list):
        for ent in words_list:
            for det, rep in ent.items():
                if rep != []:
                    words = list(map(lambda x: x.replace(det, rep[0]), words))
        sen = TreebankWordDetokenizer().detokenize(words)
        return words, sen


    def paraphrase(self, sentence, num_return_sequences=2, num_beams=2):
        model = PegasusForConditionalGeneration.from_pretrained("tuner007/pegasus_paraphrase")
        tokenizer = PegasusTokenizerFast.from_pretrained("tuner007/pegasus_paraphrase")

        input = tokenizer([sentence], truncation=True, padding="longest", return_tensors="pt")
        
        output = model.generate(
            **input,
            num_beams=num_beams,
            num_return_sequences=num_return_sequences,
        )
        output = tokenizer.batch_decode(output, skip_special_tokens=True)

        return output
    
    
    def para_txt(self, txt, pref={}):
        words_list = []
        words_data = {'dets': [], 'reps': [], 'syns': [], 'rep_dict': {}}

        words_list, words = self.filter_words(txt)
        words_list = self.filter_synonyms(words_list, pref)
        words, sen = self.replace_words(words, words_list)
        # print(words_list)
       
        for ent in words_list:
            # print(f"ent:{ent}")
            for det, rep in ent.items():
                words_data['dets'].append(det)
                words_data['reps'].append(rep[0])
                words_data['syns'].append(rep)
                words_data['rep_dict'][det] = rep[0]
        # print(words_data)
        return words_list, words_data, words, sen
    

# ml = ML()
# pred, sensitive_terms = ml.classify('the empress rules everything')
# print(pred, sensitive_terms)


para = Para_txt()
words_list, words_data, words, sen = para.para_txt('the chairman from Manila', pref={})
print(f'Words List: {words_list}')
# print(f'Data: {words_data}')
# print(f'Words: {words}')
# print(f'Sentence: {sen}')

# model = Word2Vec.load(r'C:\Users\Chester Martinez\OneDrive\Documents\School\App Dev\CapstoneProj\gadly\backend\GoogleNews-vectors-negative300.bin')
# model.wv.similarity('france', 'spain')
# print(model)