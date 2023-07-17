import nltk
from nltk.corpus import wordnet
synonyms = []
  
for syn in wordnet.synsets("stewardess"):
    for l in syn.lemmas():
        synonyms.append(l.name())

print(set(synonyms))