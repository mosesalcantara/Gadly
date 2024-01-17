# from nltk.corpus import wordnet as wn
# from nltk.wsd import lesk
# from nltk.corpus import stopwords
# import string

# stop_words = set(stopwords.words('english'))
# stop_words = stop_words.union(set(string.punctuation))

# def find_synonyms(text, word):
#     """Finds the right synonyms for a word depending on how it is used in the text."""
    
#     # Lowercase the text and remove punctuation
#     text = ' '.join(text.lower() for text in text.split())
#     stop_words = set(stopwords.words('english'))
#     stop_words = stop_words.union(set(string.punctuation))
#     tokens = [word for word in text.split() if word not in stop_words]
    
#     # Get the sentence containing the word
#     sentence = None
#     for sent in text.split('.'):
#         if word in sent.split():
#             sentence = sent
#             break
    
#     if sentence is None:
#         return []
    
#     # Use Lesk algorithm to find the correct sense of the word
#     meaning = lesk(tokens, sentence.replace('.', ''), word)
    
#     if meaning is None:
#         return []
    
#     # Find synonyms of the word in the context of the sentence
#     synonyms = set()
#     for syn in meaning.synonyms():
#         synonyms.add(syn.name())
    
#     return list(synonyms)

# # Test the function
# text = "She opened the door quickly, trying not to make any noise. She wanted to catch the burglar in the act."
# word = "quickly"
# synonyms = find_synonyms(text, word)
# print(synonyms)



# from nltk.corpus import wordnet
# syns = wordnet.synsets('word')

# definitions = []
# examples = []
# for syn in syns:
#     print(syn.name())
#     definitions.append(syn.definition())
#     examples.append(syn.examples())
# print(definitions)
# print(examples)

# import spacy

# nlp = spacy.load("en_core_web_sm")
# doc = nlp("Ethers can be named by naming two each carbon group as a separate word followed by a space with the word ether and lady guard.")
# for chunk in doc.noun_chunks:
#     print(chunk.text, chunk.root.text, chunk.root.dep_,
#             chunk.root.head.text)

# import spacy

# nlp = spacy.load("en_core_web_sm")
# doc = nlp("Ethers can be named by naming two each carbon group as a separate word followed by a space with the word ether and lady guard.")
# for token in doc:
#     print(token.text, token.pos_ ,token.dep_, token.head.text, token.head.pos_,
#             [child for child in token.children])

# from nltk.tokenize import word_tokenize, TreebankWordDetokenizer

# from nltk.corpus import wordnet as wn
from nltk.wsd import lesk

tokenized_sent = word_tokenize('the husband and wife are the lovers of the year.')
lemma_word = 'wife'
lemma_word2 = 'husband'
synsent1 = lesk(context_sentence=tokenized_sent, ambiguous_word=lemma_word, pos = 'n')
# synsent2 = lesk(context_sentence=tokenized_sent, ambiguous_word=lemma_word2, pos = 'n')

# print(synsent.name().name())

# for syn in synsent.lemmas():
#     print(syn.name())


# for ss in wn.synsets('chairman').lemmas():
#     print(ss, ss.name())

# from nltk.corpus import wordnet
# cb = wordnet.synset('cookbook.n.01')
# ib = wordnet.synset('instruction_book.n.01')
ca = synsent1.wup_similarity(synsent2)
print(ca)

