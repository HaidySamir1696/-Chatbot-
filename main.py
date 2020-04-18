from parser.pdfparser import PDFParser
import pickle
import pandas as pd
import pprint

pp = pprint.PrettyPrinter(indent=4)


############################################
### Test CDQA on HyberBus Document
############################################

filepath = './data/HyperBusSpecification.pdf'
try:
    with open('./cache/pdf-parser.pickle', 'rb') as f:
        print('Loading pdf-parser object...')
        pdfParser = pickle.load(f)
        print('Loaded...')
except:
    pdfParser = PDFParser(filepath, include_line_breaks=True)
    with open('./cache/pdf-parser.pickle', 'wb') as f:
        pickle.dump(pdfParser, f)



paragraphs = pdfParser.getData().loc[:,'paragraghs'].to_numpy()

############################################
### CDQA df
############################################
df = pd.DataFrame(columns=["title", "paragraphs"])
df = df.append({'title': 'HyperBus', 'paragraphs':paragraphs}, ignore_index=True)

from cdqa.pipeline import QAPipeline

############################################
### CDQA models

## retrival = "bm25" | "tfidf"

## reader
## # cpu version    './models/cdqa/bert_qa.joblib'
## # gpu version    './models/cdqa/bert_qa_vGPU-sklearn.joblib'
## # distilbert     './models/cdqa/distilbert_qa.joblib'
############################################
cdqa_pipeline = QAPipeline(reader='./models/cdqa/bert_qa.joblib', max_df=1.0, retriever="bm25")

cdqa_pipeline.fit_retriever(df=df)
with open('./cache/paragraphs.json', 'w') as f:
    f.write(pd.DataFrame.to_json(df))

while 1:
    query = input('Your Query: ')
    prediction = cdqa_pipeline.predict(query, n_predictions=3)

    for p in prediction:
        print('-'*30)
        print('query: {}'.format(query))
        print('answer: {}'.format(p[0]))
        print('title: {}'.format(p[1]))
        print('paragraph: {}'.format(p[2]))
        print('rank: {}'.format(p[3]))
        print('-'*30)


############################################
### Allennlp
############################################

# from allennlp.predictors.predictor import Predictor, DEFAULT_PREDICTORS
# predictor = Predictor.from_path("./models/allennlp/bidaf-model-2020.02.10-charpad.tar.gz", predictor_name=DEFAULT_PREDICTORS['bidaf'])
# x = predictor.predict(
#   passage=" context ",
#   question=" query "
# )

# print(x['best_span_str'])