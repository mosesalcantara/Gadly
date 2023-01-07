import nltk 
import random
import pyrebase

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
        
        gen_sen = db.child('data_set').child('sensitive').get()
        gen_sen = gen_sen.val()
        not_gen_sen = db.child('data_set').child('not_sensitive').get()
        not_gen_sen = not_gen_sen.val()

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
    