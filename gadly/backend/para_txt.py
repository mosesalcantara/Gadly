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

from .models import Word, Synonyms

import re

class ML():
    def __init__(self):
        f = open(r'/home/dev/gadly/gadly/backend/ML/backend/compound_words.json')
        self.compound_words = json.load(f)
        
        self.nlp =  spacy.load('en_core_web_sm')
        try: 
            self.model = load(r'/home/dev/gadly/gadly/backend/ML/joblib/model.joblib')
            self.vectorizer = load(r'/home/dev/gadly/gadly/backend/ML/joblib/vectorizer.joblib')
            self.classifier = load(r'/home/dev/gadly/gadly/backend/ML/joblib/classifier.joblib')
            self.classifier_w2v = load(r'/home/dev/gadly/gadly/backend/ML/joblib/classifier_w2v.joblib')
        except FileNotFoundError:
            self.model, self.vectorizer, self.classifier, self.classifier_w2v = self.train() 
    
    
    def train(self):    
        # print("1")
        model = KeyedVectors.load_word2vec_format(
            r'/home/dev/gadly/gadly/backend/ML/backend/GoogleNews-vectors-negative300.bin', 
            binary = True, limit = 100000)
        
        # dataset_path = r'C:\Users\Chester Martinez\OneDrive\Documents\School\App Dev\Development\gadly\backend\ML\backend\backend_dataset.csv'
        # dataset = pd.read_csv(dataset_path)
        dataset_path = open(r'/home/dev/gadly/gadly/backend/ML/backend/backend_dataset.json')
        backend_dataset = json.load(dataset_path)
        
        dataset_sen= list(set(backend_dataset['male'] + backend_dataset['female']))
        dataset_neu = list(set(backend_dataset['neutral']))
       
        num_dataset = 900
        random.shuffle(dataset_sen)
        dataset_sen = dataset_sen[:num_dataset]
        random.shuffle(dataset_neu)
        dataset_neu = dataset_neu[:num_dataset]
        
        # print(f"{len(dataset_sen)=}")
        # print(f"{len(dataset_neu)=}")
        dataset = {'word': [], 'gender': []}
        for data in dataset_sen:
            dataset['word'].append(data)
            dataset['gender'].append('sensitive')
        for data in dataset_neu:
            dataset['word'].append(data)
            dataset['gender'].append('neutral')

        
        labels = []
        features = []
        gender_sen = []
        gender_neu = []
        labels_w2v = []

        for word, gender in zip(dataset['word'], dataset['gender']):
            word = self.nlp(word)[0].lemma_

            no_prefix= word[3:]
            no_suffix= word[:-3]
            
            try:
                split_word = self.compound_words[word]
            except KeyError:
                split_word = re.split('_|-', word)
            # print(split_word)

            word_feat = {'word': split_word, 'word_length': len(word), 'prefix': [word[:4],word[:3], word[:2]], 'suffix': [word[-4:], word[-3:], word[-2:]]}
            
            features.append(word_feat)
            # if gender == 'female' or gender == 'male':
            if gender == 'sensitive':
                labels.append(1)
            else:
                labels.append(0)
            if word in model:
                if gender == 'sensitive':
                    gender_sen.append(model[word])
                    labels_w2v.append(1)
                else:
                    gender_neu.append(model[word])
                    labels_w2v.append(0)
                

        # print(f"{len(labels_w2v)=}")
        # print("2")
        
        vectorizer = DictVectorizer(sparse=False)
        features = vectorizer.fit_transform(features)
        x_train, x_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)
        # print("3")

        classifier = LogisticRegression()
        classifier.fit(x_train, y_train)
        # print(f"{classifier.score(x_test, y_test)}")
        # print("4")

        final_dataset = gender_sen + gender_neu
        classifier_w2v = LogisticRegression(max_iter= 10000)
        classifier_w2v.fit(final_dataset, labels_w2v)
        x_train_w2v, x_test_w2v, y_train_w2v, y_test_w2v = train_test_split(final_dataset, labels_w2v, test_size=0.2, random_state=42)
        # print(f"{classifier_w2v.score(x_test_w2v, y_test_w2v)}")
        
        dump(model, r'/home/dev/gadly/gadly/backend/ML/joblib/model.joblib')
        dump(vectorizer, r'/home/dev/gadly/gadly/backend/ML/joblib/vectorizer.joblib')
        dump(classifier, r'/home/dev/gadly/gadly/backend/ML/joblib/classifier.joblib')
        dump(classifier_w2v, r'/home/dev/gadly/gadly/backend/ML/joblib/classifier_w2v.joblib')
        return model, vectorizer, classifier, classifier_w2v
    
    
    def classify(self,word):
        from nltk.corpus import words
        
        word = self.nlp(word)[0].lemma_
        
        no_prefix= word[3:]
        no_suffix= word[:-3]
        
        try:
            split_word = self.compound_words[word]
        except KeyError:
            split_word = re.split('_|-', word)
        # print(split_word)
        # word_feat = {'word': word, 'word_length': len(word), 'prefix': word[:3], 'suffix': word[-3:], 'root_exist': no_prefix in words.words() or no_suffix in words.words()}
        word_feat = {'word': split_word, 'word_length': len(word), 'prefix': [word[:4],word[:3], word[:2]], 'suffix': [word[-4:], word[-3:], word[-2:]]}
        
        word_feat = self.vectorizer.transform([word_feat])
        pred = self.classifier.predict(word_feat)[0]
        
        if pred == 1:
            pass
            # print(f" {word} 1st")
        
        # Inalis ko muna ari pampagulo eh
        # if pred == 0 and word in self.model:
        #     matrix_w2v = self.model[word]
        #     matrix_w2v = np.array(matrix_w2v).reshape(1, -1)
        #     pred = self.classifier_w2v.predict(matrix_w2v)[0]
        #     if pred == 1:
        #         print(f"{word} 2nd")
        
        return pred
        
        
class Para_txt():
    def __init__(self):
        self.nlp = spacy.load('en_core_web_sm')
        # try: 
        #     self.model = load(r'C:\Users\Chester Martinez\OneDrive\Documents\School\App Dev\Development\gadly\backend\ML\joblib\model_pegasus.joblib')
        #     self.tokenizer = load(r'C:\Users\Chester Martinez\OneDrive\Documents\School\App Dev\Development\gadly\backend\ML\joblib\tokenizer_pegasus.joblib')
        # except FileNotFoundError:
        #     self.model = PegasusForConditionalGeneration.from_pretrained("tuner007/pegasus_paraphrase")
        #     self.tokenizer = PegasusTokenizerFast.from_pretrained("tuner007/pegasus_paraphrase")
        #     dump(self.model, r'C:\Users\Chester Martinez\OneDrive\Documents\School\App Dev\Development\gadly\backend\ML\joblib\model_pegasus.joblib')
        #     dump(self.tokenizer, r'C:\Users\Chester Martinez\OneDrive\Documents\School\App Dev\Development\gadly\backend\ML\joblib\tokenizer_pegasus.joblib')
            

    
        
    def filter_words(self, txt):
        words = []
        nostop = []
        nouns = []
        words_list = []
        ml = ML()
        
        words = word_tokenize(txt)
        doc = self.nlp(txt)
        # print(f"{doc=}")

                
        for word in words:
            if word.lower() not in set(stopwords.words("english")):
                nostop.append(word)        
        
        # print(f"{type(doc.ents)=}")
        # if "Christian" in doc.ents:
            # print("caasda")
        # entities = []
        # for ent in doc.ents:
        #     entities.append(str(ent.text))
        # print(f"{entities=}")
        for token in doc:
            # print(token.pos_)
            # print(f"{token.text=}")
            if (token.pos_ == 'NOUN' or token.pos_ == 'PROPN') and not any(token.i >= ent.start and token.i < ent.end for ent in doc.ents):
                nouns.append(token.text)
        # for word,tag in pos_tag(nostop):
        #     if tag.startswith('NN'):
        #         nouns.append(word) 
        
        # print(f"{nouns=}")
        for word in nouns:
            if ml.classify(word) == 1:
                words_list.append({word:[]})
        return words_list, words

    def is_plural(self, word):
        wnl = WordNetLemmatizer()
        lemma = wnl.lemmatize(word, 'n')
        return True if word is not lemma else False
    

    def get_synonyms(self, word, pref):
        syns = []
        ml = ML()
        lemma_word = ml.nlp(word)[0].lemma_
        word_rec = Word.objects.filter(word_name=lemma_word).count()
        syno_rec = Synonyms.objects.values('syno_word').filter(target_word__word_name=lemma_word)
        
        if word_rec == 1: record = True
        else: record = False
            
        if not record:
            new_word = Word.objects.create(word_name=lemma_word)
            new_word.save()

        target_word = Word.objects.get(word_name=lemma_word)
        if not record or len(syno_rec) == 0:
            for wn in wordnet.synsets(lemma_word):
                for syn in wn.lemmas():
                    if (ml.classify(syn.name()) == 0 and wordnet.synsets(syn.name())[0].pos() == 'n'):  
                        if self.is_plural(word):
                            syns.append(pluralize(syn.name()))
                        elif not self.is_plural(word):  
                            syns.append(syn.name())   
                            
                        if Synonyms.objects.filter(syno_word=syn.name(),target_word=target_word).count() == 0:
                            new_syn = Synonyms.objects.create(syno_word=syn.name(), target_word=target_word)
                            new_syn.save()    
        else:
            for row in syno_rec:
                if wordnet.synsets(row['syno_word'])[0].pos() == 'n':
                    if self.is_plural(word):
                        syns.append(pluralize(row['syno_word']))
                    elif not self.is_plural(word):
                        syns.append(row['syno_word'])
                        
        for det, rep in pref.items():
            if rep in syns:
                syns.insert(0, rep)
        syns = list(dict.fromkeys(syns))
        return syns


    def filter_synonyms(self, words_list, pref):
        # print(f"{words_list=}")
        rem_list=[]
        for ind, ent  in  enumerate(words_list):

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
    
    
    def paraphrase(self, paragraph, num_return_sequences=1, num_beams=10):
        model_name = "tuner007/pegasus_paraphrase"
        torch_device = 'cuda' if torch.cuda.is_available() else 'cpu'

        model = PegasusForConditionalGeneration.from_pretrained(model_name).to(torch_device)
        tokenizer = PegasusTokenizerFast.from_pretrained(model_name)
        # model = self.model
        # tokenizer = self.tokenizer
        doc = self.nlp(paragraph)
        sentences = []
        for sent in doc.sents:
            sentences.append(str(sent))
        final_output = []
        for sentence in sentences:
            # print(f"{sentence=}")
            input = tokenizer([sentence], truncation=True, padding="longest", return_tensors="pt")
            # print(f"{input=}")
            output = model.generate(    
                **input,
                num_beams=num_beams,
                num_return_sequences=num_return_sequences,
            )
            output = tokenizer.batch_decode(output, skip_special_tokens=True)
            # print(f"{output=}")

            final_output.append(output[0])
            
        # print(f"{final_output=}")
        final_output = "    ".join(final_output)
        # print(f"{final_output=}")
        return final_output
    
    def para_txt(self, sent, pref={}):
        words_list = [] 
        words_data = {'dets': [], 'reps': [], 'syns': [], 'rep_dict': {}}        
        
        words_list, words = self.filter_words(sent)
        # print(f"{words_list=}")
        words_list = self.filter_synonyms(words_list, pref)
        # print(f"{words_list=}")
        words, sen = self.replace_words(words, words_list)

        
        for ent in words_list:
            for det, reps in ent.items():
                words_data['dets'].append(det)
                words_data['reps'].append(reps[0])
                words_data['syns'].append(reps)
                words_data['rep_dict'][det] = reps[0]
        return words_list, words_data, words, sen


para = Para_txt()
# words_list, words_data, words, sen = para.para_txt('the chairman fireman', pref={})
txt = para.paraphrase('Wikipedia is hosted by the Wikimedia Foundation, a non-profit organization that also hosts a range of other projects.')
print(txt)
# print(f'Words List: {words_list}')
# print(f'Data: {words_data}')
# print(f'Words: {words}')
# print(f'Sentence: {sen}')