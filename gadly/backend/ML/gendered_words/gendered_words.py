from datasets import load_dataset

dataset = load_dataset("md_gender_bias", "gendered_words")
for row in dataset['train']:
    print(row)