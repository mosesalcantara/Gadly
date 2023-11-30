import spacy
from nltk.corpus import wordnet
from sklearn.metrics.pairwise import cosine_similarity

nlp = spacy.load('en_core_web_lg')

def get_wordnet_synonyms(word):
    synonyms = set()
    for syn in wordnet.synsets(word):
        for lm in syn.lemmas():
            synonyms.add(lm.name())
    return list(synonyms)

def calculate_similarity(word1, word2):
    word1_vector = nlp(word1).vector
    word2_vector = nlp(word2).vector
    return cosine_similarity([word1_vector], [word2_vector])[0][0]

def lesk_algorithm(sentence, target_word, context_word):
    context_word_synonyms = get_wordnet_synonyms(context_word)
    target_word_senses = []
    for syn in context_word_synonyms:
        print(calculate_similarity(target_word, syn))
        if calculate_similarity(target_word, syn) > 0.2:
            target_word_senses.append(syn)
    return target_word_senses

sentence = "She likes her cat's whiskers because they tickle her."
target_word = "delicious"
context_word = "shake"
synonyms = lesk_algorithm(sentence, target_word, context_word)
print(synonyms)