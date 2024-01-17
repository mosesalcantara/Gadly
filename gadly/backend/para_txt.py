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
from nltk.wsd import lesk
from pattern.en import pluralize, singularize

from transformers import PegasusForConditionalGeneration, PegasusTokenizerFast
from sklearn.feature_extraction import DictVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from gensim.models import KeyedVectors
from joblib import dump, load

from .models import Word, Synonyms, Synset



class ML():
    def __init__(self):
        f = open(r'C:\Users\Chester Martinez\OneDrive\Documents\School\App Dev\Development\gadly\backend\ML\backend\compound_words.json')
        self.compound_words = json.load(f)
        self.nlp = spacy.load('en_core_web_sm')
        
        try: 
            self.model = load(r'C:\Users\Chester Martinez\OneDrive\Documents\School\App Dev\Development\gadly\backend\ML\joblib\model.joblib')
            self.vectorizer = load(r'C:\Users\Chester Martinez\OneDrive\Documents\School\App Dev\Development\gadly\backend\ML\joblib\vectorizer.joblib')
            self.classifier = load(r'C:\Users\Chester Martinez\OneDrive\Documents\School\App Dev\Development\gadly\backend\ML\joblib\classifier.joblib')
            self.classifier_w2v = load(r'C:\Users\Chester Martinez\OneDrive\Documents\School\App Dev\Development\gadly\backend\ML\joblib\classifier_w2v.joblib')
        except FileNotFoundError:
            self.model, self.vectorizer, self.classifier, self.classifier_w2v = self.train() 
    
    
    def train(self):    
        model = KeyedVectors.load_word2vec_format(
            r'C:\Users\Chester Martinez\OneDrive\Documents\School\App Dev\GoogleNews-vectors-negative300.bin', 
            binary = True, limit = 100000
        )
        
        dataset_path = open(r'C:\Users\Chester Martinez\OneDrive\Documents\School\App Dev\Development\gadly\backend\ML\backend\backend_dataset.json')
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
            # else:
            #     vectors = []
                
            #     for word in split_word:
            #         if word in model:
            #             vectors.append(model[word])
                
            #     vectors = np.mean(vectors, axis = 0)
            #     if gender == 1:
            #         gender_sen.append(vectors)
            #     else:
            #         gender_neu.append(vectors)
            #     labels_w2v.append(gender)
                
        #     def text_to_vector(self,text):
        # words = text.split()
        # vectors = [selfmodel[word] for word in words if word in word2vec_model]
        # return np.mean(vectors, axis=0) if vectors else np.zeros(word2vec_model.vector_size)
        
        vectorizer = DictVectorizer(sparse=False)
        features = vectorizer.fit_transform(features)
        x_train, x_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)

        classifier = LogisticRegression()
        classifier.fit(x_train, y_train)
        print(f"{classifier.score(x_test, y_test)}")

        final_dataset = gender_sen + gender_neu
        classifier_w2v = LogisticRegression(max_iter= 15000)
        classifier_w2v.fit(final_dataset, labels_w2v)
        x_train_w2v, x_test_w2v, y_train_w2v, y_test_w2v = train_test_split(final_dataset, labels_w2v, test_size=0.2, random_state=42)
        print(f"{classifier_w2v.score(x_test_w2v, y_test_w2v)}")
        
        dump(model, r'C:\Users\Chester Martinez\OneDrive\Documents\School\App Dev\Development\gadly\backend\ML\joblib\model.joblib')
        dump(vectorizer, r'C:\Users\Chester Martinez\OneDrive\Documents\School\App Dev\Development\gadly\backend\ML\joblib\vectorizer.joblib')
        dump(classifier, r'C:\Users\Chester Martinez\OneDrive\Documents\School\App Dev\Development\gadly\backend\ML\joblib\classifier.joblib')
        dump(classifier_w2v, r'C:\Users\Chester Martinez\OneDrive\Documents\School\App Dev\Development\gadly\backend\ML\joblib\classifier_w2v.joblib')
        return model, vectorizer, classifier, classifier_w2v
    
   
    


    def classify(self,word):
        word = self.nlp(word)[0].lemma_
        # vectorized_data = text_to_vector(text)
        
        try:
            split_word = self.compound_words[word]
        except KeyError:
            split_word = re.split('_|-', word)
        # vectorized_data = [text_to_vector(text) for text in text_data]

        word_feat = {'word': split_word, 'word_length': len(word), 'prefix': [word[:4],word[:3], word[:2]], 'suffix': [word[-4:], word[-3:], word[-2:]]} 
        word_feat = self.vectorizer.transform([word_feat])
        
        # if word in self.model:
        #      w2vec = self.model[word]
        # else:
        #     vectors = []
                
        #     for word in split_word:
        #         if word in model:
        #             vectors.append(model[word])
                
        #     vectors = np.mean(vectors, axis = 0)
        #     w2vec = vectors
            
            # word_feat_reshaped = word_feat.reshape(1, -1)

        # print(f"{self.classifier_w2v.predict(w2vec)[0]=}")
        
        pred = self.classifier.predict(word_feat)[0]
        return pred
        
        
class Para_txt():
    def __init__(self):
        self.nlp = spacy.load('en_core_web_sm')
    
    def extract_nouns(self, text):
        doc = self.nlp(text)
        compound_nouns = []

        for token in doc:
            # print(token.text, token.pos_, token.dep_)
            if (token.pos_ == 'NOUN' or token.pos_ == 'PROPN') and not any(token.i >= ent.start and token.i < ent.end for ent in doc.ents):
                compound_noun = ''

                for child in token.children:
                    if child.dep_ == 'compound':
                        compound_noun = child.text + ' ' + compound_noun
                    # if child == doc[ind-1]:
                    #     rem_list.append(child)
                if token.dep_ != 'compound':
                    compound_nouns.append(compound_noun + token.text)

        return compound_nouns

    def filter_words(self, txt):
        words = []
        nostop = []
        nouns = []
        words_list = []
        ml = ML()
        
        words = word_tokenize(txt)
                
        for word in words:
            if word.lower() not in set(stopwords.words("english")):
                nostop.append(word)   
        nouns = self.extract_nouns(txt)
        print(f"{nouns=}")
        first_only_sen = []
        
        for word in nouns:
            if " " in word or "_" in word and ml.classify(word) == 1:
                word_split = word.split(" ")
                count = 0
                 
                if ml.classify(word_split[0]) == 1 and  all (ml.classify(word_sp) == 0 for ind, word_sp in enumerate(word_split) if ind > 0):
                    first_only_sen.append(list(word_split))
                    del word_split[0]
                    for word in word_split:
                        words_list.append({word:[]})
                else:
                    for word in word_split:
                        # print(f"{word=}")
                        if ml.classify(word) == 1:
                            words_list.append({word:[]})
                    
            
            elif ml.classify(word) == 1:
                print(f"{word=}")
                words_list.append({word:[]})
        
        to_be_removed = []
        for first_only in first_only_sen:
            final = []
            for ind, word in enumerate(words):
                for f_only in first_only:
                    if f_only == word:
                        if len(final) > 0:
                            # print(f"{ind}-{final[-1]}")
                            
                            if ind - final[-1] != 1:
                                final = []
                        final.append(ind)
                        break
                if len(final) == len(first_only_sen):
                    # print(f"{words[final[0]]=}")
                    break   
            # print(final)   
            to_be_removed.append(final[0])
        words = [elem for index, elem in enumerate(words) if index not in to_be_removed]
        print(words_list, words)
        return words_list, words

    def is_plural(self, word):
        wnl = WordNetLemmatizer()
        lemma = wnl.lemmatize(word, 'n')
        return True if word is not lemma else False
    
    

    def get_synonyms(self, word, tokenized_sent, pref):
        syns = []
        ml = ML()
        
        lemma_word = self.nlp(word)[0].lemma_
        #limited lang to sa pos NOUN
        synsent = lesk(context_sentence=tokenized_sent, ambiguous_word=lemma_word, pos = 'n')
        
        word_rec = Word.objects.filter(word_name=lemma_word).count()
        # synset_rec = Synonyms.objects.values('synset_name').filter(word__word_name=lemma_word)
        print('1')
        
        if word_rec == 1: record = True
        else: record = False
        
        if not record:
            new_word = Word.objects.create(word_name=lemma_word)
            new_word.save()
            print('2')
            
            
            # print(word_id)
            # new_synset = Synset.objects.create(synset_name = sysent.name(), word = Word.objects.get(word_name = lemma_word))
            # new_synset.save()
            # print('2')
            
            # synset_id = Synset.objects.get(synset_name = sysent.name(), word = word_id)
            # for syn in synsent.lemmas():
            #     if (ml.classify(syn.name()) == 0):
            #         syno = Synonyms.objects.create(syno_word = syn.name(), synset = synset_id)
            #         syno.save()
        
        

        synset_obj = Synset.objects.filter(word__word_name=lemma_word)
        
        synset_num = Synset.objects.filter(synset_name = synsent.name()).count()
        if synset_num == 0:
            new_synset = Synset.objects.create(synset_name = synsent.name(), word = Word.objects.get(word_name = lemma_word))
            new_synset.save()
            
        # word_get = Word.objects.get()        
        synonym_num = Synonyms.objects.filter(synset__synset_name = synsent.name()).count()
        word_get = Word.objects.get(word_name = lemma_word)
        
        if synonym_num == 0:
            synset_id = Synset.objects.get(synset_name = synsent.name(), word = word_get)
            for syn in synsent.lemmas():
                if (ml.classify(syn.name()) == 0):
                    syno = Synonyms.objects.create(syno_word = syn.name(), synset = synset_id)
                    syno.save()
                    
        synset_obj = Synset.objects.get(word__word_name=lemma_word)
        print(synset_obj)
        print("dadasdas")
        syno_from_db = Synonyms.objects.values('syno_word').filter(synset = synset_obj)
        print('1')

        for syn in syno_from_db:
            syns.append(syn['syno_word'])
        
        
        # for syn in synsent.lemmas():
        #     if (ml.classify(syn.name()) == 0):  
        #         print(syn.name())
        #         if self.is_plural(word):
        #             syns.append(pluralize(syn.name()))
        #         elif not self.is_plural(word):  
        #             syns.append(syn.name())   
                        
        # target_word = Word.objects.get(word_name=lemma_word)

        
    # def get_synonyms(self, word, tokenized_sent, pref):
        
    #     syns = []
    #     ml = ML()
    #     print(f"{word=}")
    #     lemma_word = self.nlp(word)[0].lemma_
        
        
    #     word_rec = Word.objects.filter(word_name=lemma_word).count()
    #     syno_rec = Synonyms.objects.values('syno_word').filter(target_word__word_name=lemma_word)
        
    #     if word_rec == 1: record = True
    #     else: record = False
            
    #     if not record:
    #         new_word = Word.objects.create(word_name=lemma_word)
    #         new_word.save()

    #     target_word = Word.objects.get(word_name=lemma_word)
    #     if not record or len(syno_rec) == 0:
    #         for wn in wordnet.synsets(lemma_word):
    #             for syn in wn.lemmas():
    #                 if (ml.classify(syn.name()) == 0 and wordnet.synsets(syn.name())[0].pos() == 'n'):  
    #                     if self.is_plural(word):
    #                         syns.append(pluralize(syn.name()))
    #                     elif not self.is_plural(word):  
    #                         syns.append(syn.name())   
                            
    #                     if Synonyms.objects.filter(syno_word=syn.name(),target_word=target_word).count() == 0:
    #                         new_syn = Synonyms.objects.create(syno_word=syn.name(), target_word=target_word)
    #                         new_syn.save()    
    #     else:
    #         for row in syno_rec:
    #             if wordnet.synsets(row['syno_word'])[0].pos() == 'n':
    #                 if self.is_plural(word):
    #                     syns.append(pluralize(row['syno_word']))
    #                 elif not self.is_plural(word):
    #                     syns.append(row['syno_word'])
                        
        for det, rep in pref.items():
            if rep in syns:
                syns.insert(0, rep)
        syns = list(dict.fromkeys(syns))
        
    #     word2vec_model = ml.model
    #     word_vec = word2vec_model[word]
        
    #     for syn in syns:
    #         print("have")
    #         if syn in ml.model:
                
    #             print(syn)
    #     print(f"{syns=}")
        return syns


    def filter_synonyms(self, words_list, words, pref):
        # sentence = " ".join(words)
        # print(sentence)
        # nlp = self.nlp
        # word_children = []
        # doc = nlp(sentence)
        # for token in doc:
        #     print(f"{token.text=}")
        #     word_children.append([token.text, [child for child in token.children]])
        #     print([child for child in token.children])
        # print(f"{word_children=}")
        
        rem_list=[]
        tokenized_sent = words
        for ind, ent in enumerate(words_list):
            for det, reps in ent.items():
                words_list[ind][det] = self.get_synonyms(det, tokenized_sent, pref)
                
                if not words_list[ind][det]:
                    rem_list.append(det)
        
        for name in rem_list:
            words_list = self.remove_dict(words_list, name)
        print(f"{words_list=}")
        return words_list
    
    
    def remove_dict(self, words_list, name):
        return [word for word in words_list if list(word.keys())[0] != name]


    def replace_words(self, words, words_list):
        al_rep = []
        
        for ent in words_list:
            for det, reps in ent.items():
                if det not in al_rep:
                    if reps != []:
                        words = list(map(lambda x: x.replace(det, reps[0]), words))
                al_rep.append(det)
        sen = TreebankWordDetokenizer().detokenize(words)

        return words, sen
    
    
    def para_txt(self, sent, pref={}):
        words_list = [] 
        words_data = {'dets': [], 'reps': [], 'syns': [], 'rep_dict': {}}        
        
        words_list, words = self.filter_words(sent)
        words_list = self.filter_synonyms(words_list, words, pref)
        words, sen = self.replace_words(words, words_list)

        for ent in words_list:
            for det, reps in ent.items():
                words_data['dets'].append(det)
                words_data['reps'].append(reps[0])
                words_data['syns'].append(reps)
                words_data['rep_dict'][det] = reps[0]
        return words_list, words_data, words, sen


# para = Para_txt()
# words_list, words_data, words, sen = para.para_txt('the chairman fireman and the lady guard are good', pref={})
# print(f'Words List: {words_list}')
# print(f'Data: {words_data}')
# print(f'Words: {words}')
# print(f'Sentence: {sen}')