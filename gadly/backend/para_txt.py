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

from nltk.tokenize import word_tokenize, TreebankWordDetokenizer
from nltk.corpus import stopwords, wordnet
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


class ML():
    def __init__(self):
        self.nlp =  spacy.load('en_core_web_sm')
        try: 
            self.model = load(r'/home/dev/gadly/gadly/backend/ML/joblib/model.joblib')
            self.vectorizer = load(r'/home/dev/gadly/gadly/backend/ML/joblib/vectorizer.joblib')
            self.classifier = load(r'/home/dev/gadly/gadly/backend/ML/joblib/classifier.joblib')
            self.classifier_w2v = load(r'/home/dev/gadly/gadly/backend/ML/joblib/classifier_w2v.joblib')
        except FileNotFoundError:
            self.model, self.vectorizer, self.classifier, self.classifier_w2v = self.train() 
            
    
    def preprocess(self, text):
        words = text.split()
        words = [word for word in words if word not in set(stopwords.words("english"))]
        words = pos_tag(words)
        words = [word for word, tag in words if tag.startswith('NN') or tag.startswith('JJ')]

        doc = self.nlp(text)
        ents = [ent.text for ent in doc.ents]
        words = [word for word in words if word not in ents]
        text = " ".join(words)
        return text
    
    
    def train(self):
        model = KeyedVectors.load_word2vec_format(
            r'/home/dev/gadly/gadly/backend/ML/backend/GoogleNews-vectors-negative300.bin', 
            binary = True, limit = 100000)
        dataset_path = r'/home/dev/gadly/gadly/backend/ML/backend/backend_dataset.csv'
        dataset = pd.read_csv(dataset_path)

        labels = []
        features = []
        gender_sen = []
        gender_neu = []
        labels_w2v = []

        for word, gender in zip(dataset['word'], dataset['gender']):
            word = self.nlp(word)[0].lemma_
            word_feat = {'word': word, 'word_length': len(word), 'prefix': word[:3], 'suffix': word[-3:]}
            features.append(word_feat)
            
            if gender == 'female' or gender == 'male':
                labels.append(1)
            else:
                labels.append(0)
            
            if word in model:
                if gender == 'male' or gender == 'female':
                    gender_sen.append(model[word])
                    labels_w2v.append(1)
                else:
                    gender_neu.append(model[word])
                    labels_w2v.append(0)

        vectorizer = DictVectorizer(sparse=False)
        features = vectorizer.fit_transform(features)
        x_train, x_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)

        classifier = LogisticRegression()
        classifier.fit(x_train, y_train)
        # print(f"{classifier.score(x_test, y_test)}")

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
        word = self.nlp(word)[0].lemma_
        word_feat = {'word': word, 'word_length': len(word), 'prefix': word[:3], 'suffix': word[-3:]}
        word_feat = self.vectorizer.transform([word_feat])
        pred = self.classifier.predict(word_feat)[0]

        if pred == 0 and word in self.model:
            matrix_w2v = self.model[word]
            matrix_w2v = np.array(matrix_w2v).reshape(1, -1)
            pred = self.classifier_w2v.predict(matrix_w2v)[0]
        return pred
        
        
class Para_txt():
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
        
        for word,tag in pos_tag(nostop):
            if tag.startswith('NN'):
                nouns.append(word)
                
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
        word_rec = Word.objects.values('word_id','word_name').filter(word_name=lemma_word)
        syno_rec = Synonyms.objects.values('syno_word').filter(target_word__word_name=lemma_word)
        
        if len(word_rec) > 0 and len(syno_rec) > 0: record = True
        else: record = False
            
        if not record:
            new_word = Word.objects.create(word_name=word)
            new_word.save()

        target_word = Word.objects.get(word_name=word)
        if record:
            for wn in wordnet.synsets(word):
                for syn in wn.lemmas():
                    if (ml.classify(syn.name()) == 0 and wordnet.synsets(syn.name())[0].pos() == 'n'):  
                        if self.is_plural(word):
                            syns.append(pluralize(syn.name()))
                        elif not self.is_plural(word):  
                            syns.append(syn.name())
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
        rem_list=[]
        for ind, ent  in  enumerate(words_list):
            for det, reps in ent.items():
                words_list[ind][det] = self.get_synonyms(det, pref)
                if len(words_list[ind][det]) == 0:
                    rem_list.append(ind)
            
            for ind in rem_list:
                del words_list[ind]
        return words_list


    def replace_words(self, words, words_list):
        for ent in words_list:
            for det, reps in ent.items():
                if reps != []:
                    words = list(map(lambda x: x.replace(det, reps[0]), words))
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

        for ent in words_list:
            for det, reps in ent.items():
                words_data['dets'].append(det)
                words_data['reps'].append(reps[0])
                words_data['syns'].append(reps)
                words_data['rep_dict'][det] = reps[0]
        return words_list, words_data, words, sen


# para = Para_txt()
# words_list, words_data, words, sen = para.para_txt('the chairman and fireman along with the mailman', pref={})
# print(f'Words List: {words_list}')
# print(f'Data: {words_data}')
# print(f'Words: {words}')
# print(f'Sentence: {sen}')