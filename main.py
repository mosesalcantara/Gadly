import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import wordnet
from pattern.en import pluralize, singularize
from nltk.stem import WordNetLemmatizer

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
    set_synonyms = set(synonyms)
    synonyms = list(set_synonyms)
    return synonyms

def isplural(word):
    wnl = WordNetLemmatizer()
    lemma = wnl.lemmatize(word, 'n')
    plural = True if word is not lemma else False
    return plural

sensitive = ["man", "woman", "men", "women"]
txt = input("Enter a text: ")
words = word_tokenize(txt)
stop_words = set(stopwords.words("english"))
filtered_list = []
filtered_synonyms = []
for word in words:
    if word.casefold() not in stop_words:
        filtered_list.append(word)
print(filtered_list)

for word in filtered_list:
    print (word)
    for exact_word in sensitive:
        if word == exact_word:
            #print("passed")
            pass
    for sen_word in sensitive:
        #print(sen_word)
        if sen_word in word:
            split_word = word.split(sen_word)
            #print(split_word[0])
            #print(split_word[1])
            if split_word[1] == "":
                if not wordnet.synsets(split_word[0]):
                    #print("Not an english word")
                    pass
                else:
                    if synonym_extractor(word) == 1:
                        synonyms = get_synonym(word, sensitive)
                        if isplural(word) == True:
                            for word in synonyms:
                                if isplural(word) == False:
                                    plural_word = pluralize(word)
                                    filtered_synonyms.append(plural_word)
                            print(filtered_synonyms)
                        elif isplural(word) == False:
                            print(synonyms)
                    elif synonym_extractor(word) == 0:
                        print("sala")
