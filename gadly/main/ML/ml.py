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
        # sensitive = ["man", "woman", 'men', 'women', 'boy', 'girl', 'lady', 'ess', 'her']
        sensitive = ['man', 'woman', 'men', 'women', 'boy', 'girl', 'lady', 'ess', 'her', 
                     'brother', 'sister', 'father', 'mother', 'female', 'male', 'daughter', 'son',
                     'husband', 'wife', 'queen', 'king']
        
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
        
        train_words = labeled_words[1500:]
        devtest_words = labeled_words[500:1500]
        test_words = labeled_words[:500]

        train_set = [(self.gen_sen_features(word), sen) for (word, sen) in train_words]
        devtest_set = [(self.gen_sen_features(word), sen) for (word, sen) in devtest_words]
        test_set = [(self.gen_sen_features(word), sen) for (word, sen) in test_words]
        classifier = nltk.NaiveBayesClassifier.train(train_set)
        print(nltk.classify.accuracy(classifier, devtest_set))

        errors = []
        for (word, tag) in devtest_words:
            guess = classifier.classify(self.gen_sen_features(word))
            if guess != tag:
                errors.append( (tag, guess, word) )
                
        for (tag, guess, word) in sorted(errors):
            print('correct={:<8} guess={:<8s} word={:<30}'.format(tag, guess, word))
        return classifier

    def classify(self, word):
        result = self.classifier.classify(self.gen_sen_features(word))
        return result
    
ml = ML()
ml.classify("chairman")
