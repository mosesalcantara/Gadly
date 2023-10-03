import json
import pandas as pd

        
def write_json():
    f = open(r"C:\Users\Chester Martinez\OneDrive\Documents\School\App Dev\CapstoneProj\gadly\backend\ML\gendered_words\gendered_words.json")
    json_data = json.load(f)
    dataset = {'male':[], 'female':[], 'neutral':[]}

    for row in json_data:
        if 'gender_map' in row:
            if row['gender'] == 'm' and row['word'] not in dataset['male']:
                dataset['male'].append(row['word'])
            elif row['gender'] == 'f' and row['word'] not in dataset['female']:
                dataset['female'].append(row['word'])
                
            gender = list(row['gender_map'].keys())[0]
            word = row['gender_map'][gender][0]['word']
            
            if gender == 'm' and word not in dataset['male']:
                dataset['male'].append(word)
            elif gender == 'f' and word not in dataset['female']:
                dataset['female'].append(word)
        elif row['gender'] == 'n' and row['word'] not in dataset['neutral']:
            dataset['neutral'].append(row['word'])    
    f.close()
    
    # print(dataset)
    # print(len(dataset['male']))
    # print(len(dataset['female']))
    # print(len(dataset['neutral']))

    # with open('dataset.json', 'w') as json_file:
    #     json.dump(dataset, json_file)
        
def print_json():
    f = open(r"C:\Users\Chester Martinez\OneDrive\Documents\School\App Dev\CapstoneProj\gadly\backend\ML\gendered_words\dataset.json")
    json_data = json.load(f)
    # print(json.dumps(json_data, indent=4, sort_keys=True))
    f.close()

write_json()
# print_json()