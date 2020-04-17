import json

with open('./cache/dfjson.json', 'r') as f:
    print('Loading pdf-parser object...')
    dfjson = f.read()
    dfjson = json.loads(dfjson)
    print('Loaded...')

squadLike = {"data": [{"title":dfjson["title"]["0"], "paragraphs":[]}]}
paragraphs = []
teamPar=[]

for paragraph in dfjson["paragraphs"]["0"]:
    paragraphs.append({"context":paragraph,"qas":[]})

teamNo = int(input("enter number of collaborators:"))

for i in range(0, teamNo):
    teamPar = dict(squadLike)
    teamPar["data"][0]["paragraphs"] = list(paragraphs[int((i/teamNo)*len(paragraphs)):int(((i+1)/teamNo)*len(paragraphs))])
    with open('./cache/cdqa'+str(dfjson["title"]["0"])+str(i+1)+'.json', 'w') as f:
        f.write(str(squadLike))

squadLike["data"][0]["paragraphs"] = list(paragraphs)

with open('./cache/cdqa'+str(dfjson["title"]["0"])+'.json', 'w') as f:
    f.write(str(squadLike))

# dividing files


