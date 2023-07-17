import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from .models import Data_set

# Sample data with words and their gender sensitivity labels
data = {'word': ['doctor', 'chairperson', 'nurse', 'engineer', 'she', 'chairman', 'her', 'stewardess', 'mailman', 'teacher', 'firefighter', 'secretary'],
        'gender_sensitive': [0,0, 1, 0,1,1,1,1,1,0, 0, 1]}  # 0 for not gender-sensitive, 1 for gender-sensitive

df = pd.DataFrame(data)

# Feature extraction
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(df['word'])

# Splitting the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, df['gender_sensitive'], test_size=0.2, random_state=42)

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
    if prediction == 0:
        print(f"{word} is not gender-sensitive.")
    else:
        print(f"{word} is gender-sensitive.")
