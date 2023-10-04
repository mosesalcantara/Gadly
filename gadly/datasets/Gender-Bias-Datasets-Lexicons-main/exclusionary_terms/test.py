import pandas as pd
from IPython.display import display
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

df1 = pd.read_csv("gender-neutral_sentences.csv")
df1['classifications'] = ["gender_neutral"for sentence in df1['sentences']]
# print(f"df1: {df1['classifications']}")
df2 = pd.read_csv("gendered_neologisms.csv")
df2['sentences'] = df2['definition']
df2['classifications'] = ["gender_sensitive"for sentence in df2['sentences']]


# df['classifications']  =s df1['classifications'] + df2['classifications']
df = [df1['sentences'],df2['definition']]
df = pd.concat(df)
display(df)

# print(df)
# print(f"df2: {df2['definition']}")

# gen_neu_length = [len(word) for sentence in df1['sentences'] for word in sentence.split()]
# # print(gen_neu_length)
# # df2['word'] = [word for sentence in df2['sentences'] for word in sentence.split()]
# print(df2['sentences'])
# training_data, testing_data =  train_test_split()

# df = df1[0]+df2[5]
# print(df)