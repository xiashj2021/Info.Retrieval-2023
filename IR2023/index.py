from elasticsearch import Elasticsearch
import json


es = Elasticsearch(
    ['http://10.241.8.7:9200'],
    basic_auth=('xiashj21@lzu.edu.cn', 'xiashj21'),
)

print(es.info())

json_text = 'INFO 300\IR2023\IR2023\movie.json'
with open(json_text, encoding='utf-8') as file:
    content = json.load(file)

for i, data in enumerate(content):
    doc = {
        'ranking': data['ranking'],
        'name': data['name'],
        'introduce': data['introduce'],
        'star': data['star'],
        'comments': data['comments'],
        'describe': data['describe']
    }
    # Load the doc to an index
    res = es.index(index="xiashj21_movie", id=i+1, document=doc)
    # Show results from server response
    print(res['result'])