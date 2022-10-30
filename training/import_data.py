from numpy import dtype
import pandas as pd
import os
import json

file_dir = os.path.dirname(__file__) + '\\..\\asset\\data\\'
df = pd.read_excel(file_dir + 'data.xlsx', na_filter=False)
df.fillna('')


df.to_csv(file_dir + 'data.csv', encoding='utf-8', index=False)

df = pd.read_csv(file_dir + 'data.csv')
df.fillna('', inplace=True)

data = {}

data['intents'] = []
for i in range(len(df)):
    data['intents'].append({})
    data['intents'][i]['tag'] = df['Tag'][i]
    data['intents'][i]['ques'] = df['Ques'][i].split('\n')
    data['intents'][i]['ans'] = df['Ans'][i].split('\n')
    data['intents'][i]['require'] = df['Require'][i].split('\n')

with open(file_dir + 'mind.json', 'w', encoding='utf-8') as f:
    json.dump(data, f)

with open(file_dir + 'mind.json', encoding='utf-8') as f:
    data = json.load(f)

print("Successful import data to json")
