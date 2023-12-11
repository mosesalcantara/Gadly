from nltk.corpus import wordnet as wn
from nltk.wsd import lesk
from nltk.corpus import stopwords
import string

stop_words = set(stopwords.words('english'))
stop_words = stop_words.union(set(string.punctuation))

def find_synonyms(text, word):
    """Finds the right synonyms for a word depending on how it is used in the text."""
    
    # Lowercase the text and remove punctuation
    text = ' '.join(text.lower() for text in text.split())
    stop_words = set(stopwords.words('english'))
    stop_words = stop_words.union(set(string.punctuation))
    tokens = [word for word in text.split() if word not in stop_words]
    
    # Get the sentence containing the word
    sentence = None
    for sent in text.split('.'):
        if word in sent.split():
            sentence = sent
            break
    
    if sentence is None:
        return []
    
    # Use Lesk algorithm to find the correct sense of the word
    meaning = lesk(tokens, sentence.replace('.', ''), word)
    
    if meaning is None:
        return []
    
    # Find synonyms of the word in the context of the sentence
    synonyms = set()
    for syn in meaning.synonyms():
        synonyms.add(syn.name())
    
    return list(synonyms)

# Test the function
text = "She opened the door quickly, trying not to make any noise. She wanted to catch the burglar in the act."
word = "quickly"
synonyms = find_synonyms(text, word)
print(synonyms)