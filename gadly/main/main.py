# Prerequisites
# pip install nltk
# pip install pattern

#import nltk
# nltk.download('averaged_perceptron_tagger')
# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('wordnet')
# nltk.download('omw-1.4')

import nltk
import random
import pyrebase

from nltk.tokenize import word_tokenize, TreebankWordDetokenizer
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer
from pattern.en import pluralize, singularize

config={
  "apiKey": "AIzaSyCnqRG_3w5Gb4JTlNwyMIVJs98crMBRULM",
  "authDomain": "gadly-610fb.firebaseapp.com",
  "databaseURL": "https://gadly-610fb-default-rtdb.asia-southeast1.firebasedatabase.app",
  "projectId": "gadly-610fb",
  "storageBucket": "gadly-610fb.appspot.com",
  "messagingSenderId": "350424029795",
  "appId": "1:350424029795:web:9d900d96122c6d43f97656",
  "measurementId": "G-MQYBSZQ38P"
}

firebase=pyrebase.initialize_app(config)
auth=firebase.auth()
db=firebase.database()
class ML():
    def __init__(self):
        self.classifier = self.train()
        
    def gen_sen_features(self, word):
        features = {}
        sensitive = ["man", "woman", 'men', 'women', 'boy', 'girl', 'lady', 'ess', 'her']
        
        for sen_word in sensitive:
            features["has({})".format(sen_word)] = (sen_word in word.lower())
        return features

    def train(self):
        gen_sen = []
        not_gen_sen = []
        
        gen_sen = db.child('data_set').child('sensitive').get().val()
        not_gen_sen = db.child('data_set').child('not_sensitive').get().val()

        labeled_words = ([(word, 'gen_sen') for word in gen_sen] +
                        [(word, 'not_gen_sen') for word in not_gen_sen])

        random.shuffle(labeled_words)

        featuresets = [(self.gen_sen_features(word), sensitivity) for (word, sensitivity) in labeled_words]
        train_set, test_set = featuresets[1000:], featuresets[:1000]
        
        classifier = nltk.NaiveBayesClassifier.train(train_set)
        # print(nltk.classify.accuracy(classifier, test_set))
        # classifier.show_most_informative_features(5)
        return classifier

    def classify(self, word):
        result = self.classifier.classify(self.gen_sen_features(word))
        return result
class Main():
    
    def filter_words(self, words, stop_words):
        filtered_list = []
        remove_list = []
        ml = ML()
        
        for word in words:
            if word.casefold() not in stop_words:
                filtered_list.append(word)
        for word in filtered_list:
            # word = singularize(word)
            if (ml.classify(word) == 'not_gen_sen'):
                remove_list.append(word)
        for word in remove_list:
            filtered_list.remove(word)
                    
        return filtered_list

    def get_synonym(self, word):
        synonyms = []
        filtered_synonyms = []
        ml = ML()
        
        for syn in wordnet.synsets(word):
            for lemma in syn.lemmas():
                synonyms.append(lemma.name())
        for word in synonyms:
            if (ml.classify(word) == 'not_gen_sen'):
                filtered_synonyms.append(word)
                
        filtered_synonyms = list(dict.fromkeys(filtered_synonyms))
        return filtered_synonyms
        

    def is_plural(self, word):
        wnl = WordNetLemmatizer()
        lemma = wnl.lemmatize(word, 'n')
        plural = True if word is not lemma else False
        return plural


    def filter_synonyms(self, filtered_list):
        replacement_words = []
        filtered_synonyms = []
        synonym_list = []
        remove_list = []
        rep_dict = {}
        
        for filtered_word in filtered_list:
            synonyms = self.get_synonym(filtered_word)
            if len(synonyms) != 0:
                if self.is_plural(filtered_word):
                    for word in synonyms:
                        if not self.is_plural(word):
                            plural_word = pluralize(word)
                            filtered_synonyms.append(plural_word)
                    synonym_list.append(filtered_synonyms)
                    replacement_words.append(filtered_synonyms[0])  
                    rep_dict[filtered_word] = filtered_synonyms[0]
                elif not self.is_plural(filtered_word):
                    synonym_list.append(synonyms)
                    replacement_words.append(synonyms[0])  
                    rep_dict[filtered_word] = synonyms[0]
            elif len(synonyms) == 0:
                remove_list.append(filtered_word) 
        for remove_word in remove_list:
            filtered_list.remove(remove_word)
                
        replacement_words = list(dict.fromkeys(replacement_words))
        return replacement_words, synonym_list, rep_dict


    def replace_words(self, words, filtered_list, replacement_words):
        for word in words:
            for filtered_word in filtered_list:
                index_filtered = filtered_list.index(filtered_word)
                for replacement_word in replacement_words:
                    index_replacement = replacement_words.index(replacement_word)
                    if word == filtered_word and index_filtered == index_replacement:
                        index_unfiltered = words.index(word)
                        words[index_unfiltered] = replacement_word
        return words

    def main(self, txt):
        filtered_list = []
        replacement_words = []

        words = word_tokenize(txt)
        stop_words = set(stopwords.words("english"))

        filtered_list = self.filter_words(words, stop_words)
        replacement_words, synonym_list, rep_dict = self.filter_synonyms(filtered_list)
        words = self.replace_words(words, filtered_list, replacement_words)
        sentence = TreebankWordDetokenizer().detokenize(words)
        
        return words, sentence, filtered_list, replacement_words, synonym_list, rep_dict
    