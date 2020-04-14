import json

with open('./cache/dfjson.json', 'r') as f:
    print('Loading pdf-parser object...')
    dfjson = f.read()
    dfjson = json.loads(dfjson)
    print('Loaded...')

squadLike = {"data": [{"title":dfjson["title"]["0"], "paragraphs":[]}]}
paragraphs = []

for paragraph in dfjson["paragraphs"]["0"]:
    paragraphs.append({"context":paragraph,"qas":[]})

squadLike["data"][0]["paragraphs"] = list(paragraphs)

with open('./cache/cdqa'+str(dfjson["title"]["0"])+'.json', 'w') as f:
    f.write(str(squadLike))


