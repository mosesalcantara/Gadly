import json

        
def write_json():
    f = open(r"C:\Users\Chester Martinez\OneDrive\Documents\School\App Dev\CapstoneProj\gadly\backend\ML\gendered_words\gendered_words.json")
    json_data = json.load(f)
    dataset = {'id':[], 'word':[], 'gender': []}

    for ind, row in enumerate(json_data):
        dataset['id'].append(ind)
        dataset['word'].append(row['word'])
        
        if row['gender'] == 'm':
            gender = 'male'
        elif row['gender'] == 'f':
            gender = 'female'
        elif row['gender'] == 'n':
            gender = 'neutral'
        dataset['gender'].append(gender)
    f.close()
    
    # print(dataset)
    # print(len(dataset['male']))
    # print(len(dataset['female']))
    # print(len(dataset['neutral']))

    with open('dataset.json', 'w') as json_file:
        json.dump(dataset, json_file)
        
def print_json():
    f = open(r"C:\Users\Chester Martinez\OneDrive\Documents\School\App Dev\CapstoneProj\gadly\backend\ML\gendered_words\dataset.json")
    json_data = json.load(f)
    # print(json.dumps(json_data, indent=4, sort_keys=True))
    f.close()

write_json()
# print_json()