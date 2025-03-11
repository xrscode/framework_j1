import json

with open('./src/files/totesys_data.json', 'r') as c:
    d = json.load(c)

for key in d:
    print(key)

print(d['department'][0])

