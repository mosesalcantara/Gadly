import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import wordnet

def synonym_extractor(phrase):
    synonyms = []
    for syn in wordnet.synsets(phrase):
          for l in syn.lemmas():
               synonyms.append(l.name())
    if not synonyms:
        return 0
    else:
        return 1
        print(list(synonyms))

def get_synonym(phrase, sensitive):
    synonyms = []
    for syn in wordnet.synsets(phrase):
          for l in syn.lemmas():
               synonyms.append(l.name())

    print(list(synonyms))
    for sen_word in sensitive:
        for words in synonyms:
            if sen_word in words:
                synonyms.remove(words)
    print(list(synonyms))

sensitive = ["man", "woman"]
txt = input("Enter a text: ")
words = word_tokenize(txt)
stop_words = set(stopwords.words("english"))
filtered_list = []
for word in words:
    if word.casefold() not in stop_words:
        filtered_list.append(word)
print(filtered_list)

for word in filtered_list:
    print (word)

    if word == "man" or word == "woman":
        print("passed")
    for sen_word in sensitive:
        if sen_word in word:
            split_word = word.split(sen_word)
            if split_word[1] == "":
                if not wordnet.synsets(split_word[0]):
                    print("Not an english word")
                else:
                    if synonym_extractor(word) == 1:
                        get_synonym(word, sensitive)
                    elif synonym_extractor(word) == 0:
                        print("sala")
