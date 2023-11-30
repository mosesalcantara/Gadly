import pyphen

def segment_compound_word(compound_word):
    dic = pyphen.Pyphen(lang='en_US')
    segments = dic.inserted(compound_word).split('-')
    return segments

# Example usage
compound_word = "notebook"
result = segment_compound_word(compound_word)

print(f"The segmented parts: {result}")
