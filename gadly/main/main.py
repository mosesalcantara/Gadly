# Prerequisites
# pip install nltk
# pip install pattern

#import nltk
#nltk.download('averaged_perceptron_tagger')
# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('wordnet')
# nltk.download('omw-1.4')

from nltk.tokenize import word_tokenize, TreebankWordDetokenizer
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer
from pattern.en import pluralize, singularize

from .ML.ml import ML

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

        for remove_word in remove_list:
            for word in filtered_list:
                if word == remove_word:
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
                    
                elif not self.is_plural(filtered_word):
                    synonym_list.append(synonyms)
                    replacement_words.append(synonyms[0])
                    
            elif len(synonyms) == 0:
                remove_list.append(filtered_word)
                
        for remove_word in remove_list:
            for word in filtered_list:
                if word == remove_word:
                    filtered_list.remove(word)
                
        replacement_words = list(dict.fromkeys(replacement_words))
        return replacement_words, synonym_list


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

        replacement_words, synonym_list = self.filter_synonyms(filtered_list)

        words = self.replace_words(words, filtered_list, replacement_words)

        sentence = TreebankWordDetokenizer().detokenize(words)
        
        return words, sentence, filtered_list, replacement_words, synonym_list
