import numpy as np
from keras.models import Sequential
from keras.layers import Embedding, Conv1D, GlobalMaxPooling1D, Dense

# Prepare sample data (replace with your own labeled dataset)
sentences = [
    "He is a talented engineer.",
    "She is a skilled doctor.",
    "The nurse is caring.",
    "The politician is corrupt.",
    "The teacher is knowledgeable."
]

labels = np.array([1, 1, 0, 0, 0])  # 1 indicates gender-sensitive, 0 indicates not gender-sensitive

# Text preprocessing and vectorization
word_index = {}
embedding_matrix = []  # Pretrained word embeddings or randomly initialized embeddings

# Define the maximum sequence length
max_sequence_length = 10

# Tokenize sentences and build word index
for sentence in sentences:
    for word in sentence.lower().split():
        if word not in word_index:
            word_index[word] = len(word_index) + 1
print(f"word index: {word_index}")
# Convert sentences to sequences of word indices
sequences = []
print(f"Sentence: {sentences}")
for sentence in sentences:
    sequence = [word_index[word] for word in sentence.lower().split() if word in word_index]
    sequences.append(sequence)
print(sequence)
# Pad sequences to a fixed length
padded_sequences = np.zeros((len(sequences), max_sequence_length), dtype=np.int32)
for i, sequence in enumerate(sequences):
    if len(sequence) <= max_sequence_length:
        padded_sequences[i, :len(sequence)] = sequence
    else:
        padded_sequences[i, :] = sequence[:max_sequence_length]

# Model architecture
embedding_dim = 100

model = Sequential()
model.add(Embedding(len(word_index) + 1, embedding_dim, input_length=max_sequence_length))
model.add(Conv1D(128, 5, activation='relu'))
model.add(GlobalMaxPooling1D())
model.add(Dense(64, activation='relu'))
model.add(Dense(1, activation='sigmoid'))

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Training
model.fit(padded_sequences, labels, epochs=10, batch_size=1, verbose=1)

# Calculate accuracy
loss, accuracy = model.evaluate(padded_sequences, labels)
print(f"Accuracy: {accuracy * 100:.2f}%")
