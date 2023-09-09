# import spacy
# import pandas as pd
# from sklearn.model_selection import train_test_split
# from sklearn.feature_extraction.text import TfidfVectorizer
# from sklearn.linear_model import LogisticRegression
# from sklearn.metrics import classification_report

# # Load the spaCy English model
# nlp = spacy.load("en_core_web_sm")
# print("Ss")
# # Sample dataset with sentences and labels
# data = {
#     'sentences': [
#         "chairman is a great programmer.",
#         "She is an excellent engineer.",
#         "The doctor is really skilled.",
#         "The nurse is caring and compassionate.",
#         "The chef prepares delicious meals.",
#         "The teacher is knowledgeable.",
#         "The secretary handles administrative tasks.",
#         "The firefighter bravely rescues people.",
#         "The police officer enforces the law.",
#         "The artist creates beautiful paintings."
#     ],
#     'labels': [1, 1, 0, 0, 0, 0, 0, 0, 0, 0]  # 1 for gender-sensitive, 0 for not gender-sensitive
# }

# df = pd.DataFrame(data)

# # Splitting the data
# X_train, X_test, y_train, y_test = train_test_split(df['sentences'], df['labels'], test_size=0.2, random_state=42)

# # Feature extraction
# vectorizer = TfidfVectorizer()
# X_train_vec = vectorizer.fit_transform(X_train)
# X_test_vec = vectorizer.transform(X_test)

# # Model training
# model = LogisticRegression()
# model.fit(X_train_vec, y_train)

# # Model evaluation
# y_pred = model.predict(X_test_vec)
# report = classification_report(y_test, y_pred, target_names=["Not Gender-Sensitive", "Gender-Sensitive"])
# print(report)

# # Identify and print gender-sensitive words
# gender_sensitive_words = set()

# for sentence in df['sentences']:
#     doc = nlp(sentence)
#     for token in doc:
#         if token.pos_ == "NOUN" and token.dep_ != "compound":
#             gender_sensitive_words.add(token.text)
# print("asa")
# print("Gender-sensitive words:", gender_sensitive_words)
