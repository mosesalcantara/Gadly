# Prerequisites
# pip install nltk
# pip install pattern

#import nltk
#nltk.download('averaged_perceptron_tagger')
# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('wordnet')
# nltk.download('omw-1.4')

from nltk.tokenize import sent_tokenize, word_tokenize, TreebankWordDetokenizer
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer
from pattern.en import pluralize, singularize

class Main():
    def filter_words(self, words, stop_words, sensitive):
        filtered_list = []
        remove_list = []
        for word in words:
            if word.casefold() not in stop_words:
                filtered_list.append(word)
        # print("Remove Stop Words")
        # print(filtered_list)

        for word in filtered_list:
            detection = 0
            for sen_word in sensitive:
                if sen_word in word:
                    detection += 1
            if detection == 0:
                remove_list.append(word)

        for remove_word in remove_list:
            for word in filtered_list:
                if word == remove_word:
                    filtered_list.remove(word)

        for sen_word in sensitive:
            for word in filtered_list:
                if sen_word in word:
                    if word == sen_word:
                        remove_list.append(word)
                    else:
                        split_word = word.split(sen_word)
                        if split_word[0] and split_word[1]:
                            filtered_list.remove(word)
                        elif not split_word[0]:
                            if not wordnet.synsets(split_word[1]):
                               #if split_word[1] != "ing":#mothering, fathering, etc. gender sensitive yun pwede ipang condition to 
                                remove_list.append(word)
                        elif not split_word[1]:
                            if not wordnet.synsets(split_word[0]):
                                remove_list.append(word)
                                
                        #itong nasa baba yung orig, ineedit ko yung algo at code kasi may flaws kasi pwedeng nasa unahan yung word na pertaining sa gender such as mankind, mothering
                        '''
                        split_word = word.split(sen_word)
                        if split_word[1]:
                            filtered_list.remove(word)
                        elif not split_word[1]:
                            if not wordnet.synsets(split_word[0]):
                                remove_list.append(word)'''

        for remove_word in remove_list:
            for word in filtered_list:
                if word == remove_word:
                    filtered_list.remove(word)
        return filtered_list


    def get_synonym(self, word, sensitive):
        synonyms = []
        for syn in wordnet.synsets(word):
            for lemma in syn.lemmas():
                synonyms.append(lemma.name())
        for sen_word in sensitive:
            for words in synonyms:
                if sen_word in words:
                    synonyms.remove(words)
        synonyms = list(dict.fromkeys(synonyms))
        return synonyms
        

    def is_plural(self, word):
        wnl = WordNetLemmatizer()
        lemma = wnl.lemmatize(word, 'n')
        plural = True if word is not lemma else False
        return plural


    def filter_synonyms(self, filtered_list, sensitive):
        replacement_words = []
        filtered_synonyms = []
        synonym_list = []
        for filtered_word in filtered_list:
            synonyms = self.get_synonym(filtered_word, sensitive)
            # synonym_list.append(synonyms)
            if len(synonyms) != 0:
                # print(filtered_word)
                if self.is_plural(filtered_word):
                    for word in synonyms:
                        if not self.is_plural(word):
                            plural_word = pluralize(word)
                            filtered_synonyms.append(plural_word)
                    # print(filtered_synonyms)
                    synonym_list.append(filtered_synonyms)
                    replacement_words.append(filtered_synonyms[0])
                elif not self.is_plural(filtered_word):
                    # print(synonyms)
                    synonym_list.append(synonyms)
                    replacement_words.append(synonyms[0])
            elif len(synonyms) == 0:
                filtered_list.remove(filtered_word)
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
        sensitive = ["man", "woman", "men", "women", "lady", "boy", "girl", "mother", "father"]
        # txt = input("Enter a text: ")
        filtered_list = []
        filtered_synonyms = []
        replacement_words = []

        words = word_tokenize(txt)
        # print("Split Sentence Into Words")
        # print(words)
        stop_words = set(stopwords.words("english"))

        filtered_list = self.filter_words(words, stop_words, sensitive)
        # print("Get Gender-Sensitive Words")
        # print(filtered_list)

        # print("Get Synonyms")
        replacement_words, synonym_list = self.filter_synonyms(filtered_list, sensitive)
        # print("Filtered List")
        # print(filtered_list)
        # print("Replacement Words")
        # print(replacement_words)
        #
        # print("Original Sentence Split Into Words")
        # print(words)

        words = self.replace_words(words, filtered_list, replacement_words)
        # print("Revised Sentence Split into Words")
        # print(words)

        sentence = TreebankWordDetokenizer().detokenize(words)
        # print("Revised Sentence")
        # print(sentence)
        return words, sentence, filtered_list, replacement_words, synonym_list
