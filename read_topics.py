import json

with open('topics.json', 'r') as f:
    topics = json.load(f)
    
for i in topics['data']:
    print(i['topic_name'])
