import json

f = open('data_set.json')

data = json.load(f)

count = 0

f1 = open("gen_sen.txt", "w")

for i in data:
    if (i['gender'] == 'm' and count < 500):
        count += 1
        f1.write(i['word']+'\n')
        
count = 0       
f1.close()

f1 = open("gen_sen.txt", "a")

for i in data:
    if (i['gender'] == 'f' and count < 500):
        count += 1
        f1.write(i['word']+'\n')
        
count = 0
f1.close()

f1 = open("not_gen_sen.txt", "w")

for i in data:
    if (i['gender'] == 'n' and count < 1000):
        count += 1
        f1.write(i['word']+'\n')
        
count = 0       
f1.close()

f.close()