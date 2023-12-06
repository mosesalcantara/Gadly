import pandas as pd
import json

csv_data = pd.read_csv('LADEC_hyponymy_dataset_2020_February25.csv')
# csv_data = pd.read_csv('LADEC_SemanticTransparency_FactorAnalysis.csv')

dataset = {}
for first_word, second_word, whole_word in zip(csv_data['c1'], csv_data['c2'], csv_data['stim']):
    dataset[whole_word] = (first_word, second_word)
json_string = json.dumps(dataset)

with open('compound_words.json', 'w') as f:
    f.write(json_string)
