
from nltk.tokenize import sent_tokenize, word_tokenize
import nltk.corpus

text = word_tokenize("And now for something completely different")
c =nltk.pos_tag(text)
for a in c:
    print (a)