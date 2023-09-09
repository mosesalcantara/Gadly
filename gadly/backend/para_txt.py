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
# # model = KeyedVectors.load_word2vec_format(model_path, binary=True)
# word_vectors = KeyedVectors.load_word2vec_format(model_path, binary=True, limit=500000)

# labeled_data = [('king', 'male'), ('queen', 'female'), ('doctor', 'neutral'), ('nurse', 'neutral')]
# trained_classifier, accuracy = gender_classification_model(model_path, labeled_data)

class ML():
    def __init__(self):
        model_path = 'GoogleNews-vectors-negative300.bin'
        self.word_vectors = KeyedVectors.load_word2vec_format(model_path, binary=True, limit=80000)
        self.vectorizer = CountVectorizer()
        # self.vectorizer1 = CountVectorizer()
        self.vectorizer_gen_class = CountVectorizer()

        self.model = self.train()
        self.model1 = self.train_gen_class()
    def train_gen_class(self):
        dataset = Dataset.objects.exclude(gen__isnull=True)
        # for data in dataset
        #     print(data.word)
        # word_embeddings = [self.word_vectors[data.word.replace("\n", "").replace("_", " ")] for data in dataset]

        # print(f"{word_embeddings=}")
        # word_embeddings = []

        # for data in dataset:

        #     cleaned_word = data.word.replace("\n", "").replace("_", " ")
            
        #     if cleaned_word in self.word_vectors:
        #         word_vector = self.word_vectors[cleaned_word]
            
        #         word_embeddings.append(word_vector)
                
        #         print(f"Processing word: {cleaned_word}")
        # print(len(word_embeddings))
        # Now you have the word embeddings in the word_embeddings list


        # print(self.word_vectors['abbot'])
        words = [data.word for data in dataset]
        labels = [data.gen for data in dataset]
        word_lengths = [len(word) for word in words]
        # if 'woman' in word
        print("success2")

        suffixes = [word[-3:] for word in words]
        # suffixes = [word[-5:] if 'woman' in word else word[-3:] for word in words]s
        # prefixes = [word[:5] if 'woman' in word else word[:3] for word in words]
        prefixes = [word[:3] for word in words]
        features = [f"{word} {length} {suffix} {prefix}" for word, length, suffix, prefix in zip(words, word_lengths, suffixes, prefixes)]
        print("success3")
        self.vectorizer_gen_class.fit(features)
        X = self.vectorizer_gen_class.transform(features)
        print("success5")

        X_train, X_test, y_train, y_test = train_test_split(X, labels, test_size=0.2, random_state=42)
        print("success6")

        model = LogisticRegression()
        model.fit(X_train, y_train)
        print("success7")

        accuracy = model.score(X_test, y_test)  
        print("Gen_class_Accuracy:", accuracy)

        return model
    
    def gender_classification_model(self, word):
        print((f"Word: {word}"))
        length = len(word)
        suffix = word[-3:]
        prefix = word[:3]
        feature = f"{word} {length} {suffix} {prefix}"
        print("success8")

        X_new = self.vectorizer_gen_class.transform([feature])
        print(f"X_new: {X_new}")
        prediction = self.model1.predict(X_new)[0]
        
        # 
        print(f"Prediction: {prediction}")
        return prediction


        # # Prepare the data    
        # words, labels = zip(*labeled_data)

        # # Convert words to word vectors
        # word_vectors_data = [word_vectors[word] if word in word_vectors else np.zeros(300) for word in words]

        # # Split data into training and testing sets
        # X_train, X_test, y_train, y_test = train_test_split(word_vectors_data, labels, test_size=test_size, random_state=random_state)

        # # Train a logistic regression classifier
        # classifier = LogisticRegression()
        # classifier.fit(X_train, y_train)

        # # Make predictions on the test data
        # y_pred = classifier.predict(X_test)

        # # Calculate accuracy
        # accuracy = accuracy_score(y_test, y_pred)

        # return classifier, accuracy



    # print(f"Classifier Accuracy: {accuracy * 100:.2f}%")

    # # Predict gender for new words
    # new_words = ['actor', 'actress', 'engineer', 'scientist']
    # new_word_vectors = [word_vectors[word] if word in word_vectors else np.zeros(300) for word in new_words]
    # # predicted_genders = trained_classifier.predict(new_word_vectors)

    # print("Predicted Genders for New Words:")
    # for word, gender in zip(new_words, predicted_genders):
    #     print(f"{word}: {gender}")

    def train(self):
        dataset = Dataset.objects.all()
        words = [data.word for data in dataset]
        labels = [data.sen for data in dataset]

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
        print((f"Word: {word}"))
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
        return prediction
        # print(f"Prediction: {prediction}")
        


class Para_txt():

    def filter_words(self, txt):
        nostop_words = []
        nouns = []
        words_dict = {}
        count = 0
        print("success1")
        ml = ML()
        print("success ML")

        words = word_tokenize(txt)
        stop_words = set(stopwords.words("english"))
        print("success1")

        for word in words:
            if word.lower() not in stop_words:
                nostop_words.append(word)        
        tagged_words = pos_tag(nostop_words)
        # print(tagged_words)
        print("success1")

        for word,tag in tagged_words:
            if tag.startswith('NN') or tag == 'JJ':
                nouns.append(word)
        print(f"Nonuns: {nouns}")
        print(f"ate:{ml.classify('Ate')}")
        for word in nouns:
            # if ml.classify(word) == 'gen_sen':
            # print(f"ML Classify: {ml.classify(word)}")
            
            if ml.classify(word) == 'gen_sen':
                print(f"Wordnouns: {word}")

                gen_class = ml.gender_classification_model(word)
                # print(gen_class)
                print(f"Wordnouns: {word}")
                # print(f"ML Classify: {ml.classify(word)}")

                words_dict[count] = {word: [], 'gen_class': gen_class}
                count += 1

        print(f"word_dict: {words_dict}")
        return words_dict, words

    def get_synonyms(self, word, gen_class, pref):
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
        print(f"word dict: {words_dict}")
        print(words_dict)
        count = 0
        for ind, ent in words_dict.items():
            # print(f"ind: {ind}, ent: {ent}")
            # count = 0
            # print(ent[0])
            for det, rep in ent.items():
                print(f"{det=}")
                if det != 'gen_class':
                    print(f"det: {det} rep: {rep}")
                    words_dict[ind][det] = self.get_synonyms(det, words_dict[count]['gen_class'], pref)
                    if len(words_dict[ind][det]) == 0:
                        rem_list.append(ind)
            count = count + 1
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
        print("para_txt")
        words_dict, words = self.filter_words(txt)
        print("dibe filter words")
        # print(f"words_dict: {words_dict[0]['gen_class']}")
        print(f"words_dict before filter synonyms{words_dict}")
        words_dict = self.filter_synonyms(words_dict, pref)
        print(words_dict)
        words, sen = self.replace_words(words, words_dict)
        print("okay na")
        for ind, ent in words_dict.items():
            print(f"ent:{ent}")
            for det, rep in ent.items():
                words_data['dets'].append(det)
                words_data['reps'].append(rep[0])
                words_data['syns'].append(rep)
                words_data['rep_dict'][det] = rep[0]
                
        # print(words_data)
        return words_dict, words_data, words, sen
    





#     def get_synonyms(self, word, gen_class, pref):
#         print(f"gen_class: {gen_class}")
#         syns = []
#         ml = ML()
#         # Calculate gender bias vectors
#         men = ['man', 'boy', 'guy', 'lad', 'man', 'men']
#         women = ['women', 'girl', 'lady', 'woman', 'ladies'] 
#         sum_men_vec = 0
#         for man in men:
#             ml.word_vectors[man] + sum_men_vec
#         avg_bias_man = sum_men_vec/len(men)

#         sum_women_vec = 0
#         for woman in women:
#             ml.word_vectors[woman] + sum_women_vec
#         avg_bias_woman = sum_women_vec/len(women)
        
#         # gender_bias_man = ml.word_vectors['man'] - ml.word_vectors['woman']
#         # gender_bias_woman = ml.word_vectors['woman'] - ml.word_vectors['man']
#         gender_bias_man = avg_bias_man - avg_bias_woman
#         gender_bias_woman = avg_bias_woman - avg_bias_man

#         # Get the word vector for the input word
#         input_vector = ml.word_vectors[word]
#         # word = 'chairman'
#         synonyms = [synonym for synonym, _ in ml.word_vectors.most_similar(word, topn=5)]
#         print(synonyms)
#         # print(f"Most similart to {input_vector}: {ml.word_vectors.most_similar_words(input_vector, topn = 10)}")
#         # Calculate the gender-neutral vector for the input word
#         if gen_class=='masculine':
#             gender_neutral_vector = input_vector - gender_bias_woman
#         elif gen_class == 'feminine':
#             gender_neutral_vector = input_vector - gender_bias_man
#         # # else:
#         # gender_neutral_vector = input_vector
#         similar_words = ml.word_vectors.similar_by_vector(gender_neutral_vector, topn=5)
        
#         # Filter out any words that contain 'man' or 'woman' to ensure gender neutrality
#         # gender_neutral_synonyms = [word for word, _ in similar_words if 'man' not in word.lower() and 'woman' not in word.lower()]
#         gender_neutral_synonyms = [word for word, _ in similar_words if ml.classify(word) != 'gen_sen']
#         # gender_neutral_synonyms = [word for word, _ in similar_words] 


#         count = 0
#         for gns in gender_neutral_synonyms:
#             if self.is_plural(word):
#                 gender_neutral_synonyms[count] = pluralize(gns)
#             elif not self.is_plural(word):
#                 gender_neutral_synonyms[count] = singularize(gns)
#             count = count + 1

#         print(gender_neutral_synonyms)


#         # for wn in wordnet.synsets(word):
#         #     for syn in wn.lemmas():
#         #         if (ml.classify(syn.name()) == 'not_gen_sen'):
#         #             if self.is_plural(word):
#         #                 syns.append(pluralize(syn.name()))
#         #             elif not self.is_plural(word):
#         #                 syns.append(syn.name())

#         # for det, rep in pref.items():
#         #     if rep in syns:
#         #         syns.insert(0, rep)
#         # syns = list(dict.fromkeys(syns))

#         syns = list(dict.fromkeys(gender_neutral_synonyms))
#         print(f"Synonyms: {syns}")
#         return syns

# # obj = Main()
# # words_dict, words_data, words, sen = obj.main('the chairman is also a fine firemen along with a mailman', pref={})
# # print(f'Words Dictionary: {words_dict}')
# # print(f'Data: {words_data}')
# # print(f'Words: {words}')
# # print(f'Sentence: {sen}')
