# import spacy

# nlp = spacy.load("en_core_web_sm")

# def extract_nouns(text):
#     doc = nlp(text)
#     compound_nouns = []

#     for token in doc:
#         print(token.text, token.pos_, token.dep_)
#         if (token.pos_ == 'NOUN' or token.pos_ == 'PROPN') and not any(token.i >= ent.start and token.i < ent.end for ent in doc.ents):
#             compound_noun = ''

#             for child in token.children:
#                 if child.dep_ == 'compound':
#                     compound_noun = child.text + ' ' + compound_noun
#                 # if child == doc[ind-1]:
#                 #     rem_list.append(child)
#             if token.dep_ != 'compound':
#                 compound_nouns.append(compound_noun + token.text)

#     return compound_nouns


import nltk
from nltk.corpus import wordnet
from nltk.wsd import lesk

def get_sense_ids(text):
    # Tokenize the text into words
    words = nltk.word_tokenize(text)
    synsets = lesk(context_sentence= words, ambiguous_word= 'men', pos = 'n')
    print( synsets)
    for synset in synsets.lemmas():
        print(synset.name())

text = " His men was killed by the enemy military."
get_sense_ids(text=text)
    