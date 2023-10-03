import json

f = open('data_set.json')
data = json.load(f)
f.close()

males=[]
females=[]
neutrals=[]

for row in data:
    if (row['gender']=='m'):
        males.append(row['word'])   
    elif (row['gender']=='f'):
        females.append(row['word'])
    elif (row['gender']=='n'):
        neutrals.append(row['word'])

males = list(dict.fromkeys(males))
females = list(dict.fromkeys(females))
neutrals = list(dict.fromkeys(neutrals))

# print('Males: ', len(males))
# print('Females: ', len(females))
# print('Neutrals: ', len(neutrals))

f = open('males.txt', 'w')
for word in males[:365]:
    f.write(word+'\n') 
f.close()    

f = open('females.txt', 'w')
for word in females[:365]:
    f.write(word+'\n')
f.close()

f = open('neutrals.txt', 'w')
for word in neutrals[:730]:
    f.write(word+'\n')
f.close()