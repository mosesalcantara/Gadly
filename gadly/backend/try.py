# import spacy

# nouns = []
# nlp = spacy.load("en_core_web_sm")
# doc = nlp("Mankind's racing cars shift insurance liability toward manufacturers")
# head_txt = ""
# for token in doc:
#     if token.text != head_txt:
#         if (token.pos_ == 'NOUN' or token.pos_ == 'PROPN') and not any(token.i >= ent.start and token.i < ent.end for ent in doc.ents):
#             word = token.text
#             if token.dep_ == 'compound':
#                 word = token.text + " " + token.head.text
#                 head_txt = token.head.text
#             nouns.append(word)
#         # print(token.text, token.dep_, token.head.text, token.head.pos_,
#         #         [child for child in token.children])
# print(nouns)

# from nltk.corpus import sentiwordnet as swn
# sentisynset = swn.senti_synset('lady_guard')
# print(sentisynset)

import nltk
from nltk.util import ngrams
from nltk.corpus import wordnet

def get_synonyms(word):
    synonyms = []
    for syn in wordnet.synsets(word):
        for lm in syn.lemmas():
            synonyms.append(lm.name())
    return synonyms

# This is the sentence from which we want to get the synonyms
sentence = "Python is an interpreted high-level programming language"

# Here we get the n-grams of the sentence. We'll consider n=3.
n_grams = ngrams(sentence.split(), 3)

# This will store the final output
final_output = []

for gram in n_grams:
    synonyms = []
    for word in gram:
        synonyms.append(get_synonyms(word))
    final_output.append(synonyms)

print(final_output)