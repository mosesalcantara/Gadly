import pandas as pd
import json
import csv
# JSON data
f = open(r"C:\Users\Chester Martinez\OneDrive\Documents\School\App Dev\CapstoneProj\gadly\backend\ML\gendered_words\gendered_words.json")
json_data = json.load(f)
final_rows = []
# Convert JSON data to DataFrame
for ind, row in enumerate(json_data):
    n_row = []
    gender = ""
    if row['gender'] == 'f':
        gender = 'female'
    elif row['gender'] == 'm':
        gender = 'male'
    elif row['gender'] == 'n':
        gender = 'neutral'
    n_row = [ind, row['word'], gender]
    final_rows.append(n_row)
print(final_rows)
fields = ['word_id', 'word', 'gender']
filename = 'output.csv'
with open(filename, 'w') as csvfile:  
    csvwriter = csv.writer(csvfile)  
    
    # writing the fields  
    csvwriter.writerow(fields)  
        
    # writing the data rows  
    csvwriter.writerows(final_rows)
    
    