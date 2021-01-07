from bs4 import BeautifulSoup
import json

data = None
jdict = None
with open('/home/artiste/quizlet/dicts/edict.json') as infile:
    jdict=json.loads(infile.read())
with open('freq.html', 'r') as infile:
    data = infile.read()
soup = BeautifulSoup(data, 'html.parser')
ol = soup.find('ol')
items = ol.findAll('li')
result = {}
for index, item in enumerate(items):
    print(index)
    word = None
    if item.find('a') == None:
        word = item.get_text()
    else:
        word = item.find('a').get_text()
    definitions = None
    if word in jdict.keys():
        definitions = jdict[word]
    rank = index + 1
    result[rank] = {'word':word, 'rank':rank, 'definitions':definitions}
with open('freq-data', 'w') as outfile:
    outfile.write(json.dumps(result, ensure_ascii=False))
print(result)

