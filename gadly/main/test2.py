import pandas as pd
from .models import Data_set

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression

# Assuming you have already defined the Data_set model

# Retrieve the data from the Data_set model
dataset = Data_set.objects.all()

# Preprocess the data to extract the words and gender sensitivity labels
words = [data.word for data in dataset]
labels = [data.sen for data in dataset]

# Feature extraction
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(words)

# Splitting the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, labels, test_size=0.2, random_state=42)

# Training the model
model = LogisticRegression()
model.fit(X_train, y_train)

# Predicting on test data
y_pred = model.predict(X_test)

# Evaluating the model
accuracy = (y_pred == y_test).mean()
print("Accuracy:", accuracy)

# Classifying new words
new_words = ['pilot', 'nanny', 'engineer', 'waiter']
X_new = vectorizer.transform(new_words)
predictions = model.predict(X_new)

for word, prediction in zip(new_words, predictions):
    if prediction == 'not gender-sensitive':
        print(f"{word} is not gender-sensitive.")
    else:
        print(f"{word} is gender-sensitive.")
