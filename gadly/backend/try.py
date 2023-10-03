from datasets import load_dataset
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from gensim.models import KeyedVectors, Word2Vec

import matplotlib.pyplot as plt
import numpy as np
import spacy
import json

model_path = r'C:\Users\Chester Martinez\OneDrive\Documents\School\App Dev\CapstoneProj\gadly\backend\ML\GoogleNews-vectors-negative300.bin'
# word_vectors = KeyedVectors.load_word2vec_format(model_path, binary=True, limit = 1500000)
f = open(r"C:\Users\Chester Martinez\OneDrive\Documents\School\App Dev\CapstoneProj\gadly\backend\ML\opensubtitles_inferred\opensubtitles_inferred.json")
os_ds = json.load(f)

def classify():
    train_os_ds = os_ds['train'] 
    test_os_ds = os_ds['test']
    val_os_ds = os_ds['validation']

    os_text = [text for text in train_os_ds['text']]
    os_text.extend(test_os_ds['text'])
    os_text.extend(val_os_ds['text'])
    
    os_labels = [label for label in train_os_ds['label']]
    os_labels.extend(test_os_ds['label'])
    os_labels.extend(val_os_ds['label'])
    
    text = os_text
    init_labels = os_labels
    
    labels = []
    for item in init_labels:
        if item == 1 or item == 0:
            labels.append(1)
        else:
            labels.append(0)

    tfidf_vec = TfidfVectorizer(stop_words='english', use_idf= True)
    x = tfidf_vec.fit_transform(text)
    # print(tfidf_vec.vocabulary_)
    # print(tfidf_vec.get_feature_names_out())
    
    classifier = LogisticRegression(max_iter= 10000)
    classifier.fit(x,labels)
    feat_names = tfidf_vec.get_feature_names_out()
    coefs_feat_names = sorted(zip(classifier.coef_[0], feat_names), reverse=True)
    x_train, x_test, y_train , y_test = train_test_split(x, labels, test_size=0.2, random_state=42)

    sentence = str(input("Input a sentence: "))
    retrieval_vec = TfidfVectorizer(stop_words='english', use_idf= True)
    retrieval_matrix = retrieval_vec.fit_transform([sentence])
    # print(retrieval_vec.vocabulary_)
    sensitive_terms = []
    for ret_feat_name in retrieval_vec.get_feature_names_out():
        for coef, feat_name in coefs_feat_names:
            if ret_feat_name == feat_name and coef >= 0.5:
                sensitive_terms.append(ret_feat_name)
    print(sensitive_terms)
            
    matrix = tfidf_vec.transform([sentence])
    prediction = classifier.predict(matrix)
    # print(prediction)
    if prediction == 1:
        print('gender_sensitive')
    else:
        print('gender_neutral') 
        
    print(f"{classifier.score(x_test, y_test)*100=}")
    classify()


def write_json():
    os_dict = {'train':{'text':os_ds['train']['text'], 'label':os_ds['train']['ternary_label']},
               'validation':{'text':os_ds['validation']['text'], 'label':os_ds['validation']['ternary_label']},
               'test':{'text':os_ds['test']['text'], 'label':os_ds['test']['ternary_label']},
               }
    with open(r'C:\Users\Chester Martinez\OneDrive\Documents\School\App Dev\CapstoneProj\gadly\backend\ML\opensubtitles_inferred\opensubtitles_inferred.json', 'w') as json_file:
        json.dump(os_dict, json_file)
        
        
def read_json():
    f = open(r"C:\Users\Chester Martinez\OneDrive\Documents\School\App Dev\CapstoneProj\gadly\backend\ML\opensubtitles_inferred\opensubtitles_inferred.json")
    json_data = json.load(f)
    # label: 0 = female, 1 = male, 2 = neutral
    
    
def show_most_informative_features(vectorizer, clf, n=50):
    feature_names = vectorizer.get_feature_names_out()
    coefs_with_fns = sorted(zip(clf.coef_[0], feature_names), reverse=True)
    top = coefs_with_fns[:n]
    for (coef, fn) in top:
        print("\t%.4f\t%-15s" % (coef, fn))
    
    
classify()
print('Done')
# write_json()
# read_json()