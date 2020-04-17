
import os
import pandas as pd
from ast import literal_eval
from cdqa.utils.converters import pdf_converter
from cdqa.utils.filters import filter_paragraphs
from cdqa.pipeline import QAPipeline
from cdqa.utils.download import download_model

# for figures and tables
import PyPDF2
# import fitz
import pandas as pd
from PIL import Image
import webbrowser
global CDQA_PIPELINE
CDQA_PIPELINE = None


#use the handle figure FUNCTION
pdf_scr = './data_pdf/pdf/HyperBusSpecification.pdf'
img_src = "./data_pdf/pdf/out.png"
pdf_dir = "./data_pdf/pdf"
csv_file = "./data_pdf/csv/converted_pdfs.csv"
model_file = "./models/cdqa/bert_qa.joblib"



def init_cdqa_pipeline(csv_file, model_file) -> QAPipeline:
    df = pd.read_csv(csv_file, converters={'paragraphs': literal_eval})
    #df = filter_paragraphs(df, min_length=20)
    #cdqa_pipeline = QAPipeline(reader= model_file, retriever=“bm25“)
    #cdqa_pipeline = QAPipeline(reader=model_file, retriever="tfidf")
    cdqa_pipeline = QAPipeline(reader=model_file, max_df=1.0)
    cdqa_pipeline.fit_retriever(df=df)
    return cdqa_pipeline



### THE NEXT CELL IS A FUNCTION FOR DEALING WITH FIGURES IN THE PDF
#pdf_dir refers to the path of the directory of pdfs only
#pdf_scr refers to the path of a certain pdf file
#img_scr refers to the path to save the temprory image produced by the function

# def handle_figures(pdf_dir,pdf_scr,img_src,prediction):
#     # creating a pdf file object
#     pdfFileObj = open(pdf_scr, 'rb')

#     # creating a pdf reader object
#     pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
#     para = prediction[2]

#     # creating a page object
#     for page in range(pdfReader.numPages):
#         # creating rotated page object
#         pageObj = pdfReader.getPage(page)
#         txt= pageObj.extractText()
#         txt2 =txt.replace('\n', '')

#          #check to return the image
#         if(txt2.find(para)!=-1 and (para.split(None, 1)[0] == "Figure" or para.split(None, 1)[0] == "Table")):

#             # code for highlighting the figures and produce the image
#             doc = fitz.open(pdf_scr)
#             page2 = doc[page]
#             #print(page2)
#             text_instances = page2.searchFor(para)
#             #print(text_instances)

#             # HIGHLIGHT
#             for inst in text_instances:
#                 highlight = page2.addHighlightAnnot(inst)

#             ### OUTPUT IMAGE
#             pix = page2.getPixmap()
#             out = "out.png"
#             pix.writePNG(img_src)
#             img = Image.open(img_src)
#             img.show()
#             #print(page+1)

#             #remove the image
#             for img_file in os.listdir(pdf_dir):
#                 if img_file.endswith(".png"):
#                     os.remove(img_src)

#             #break from the whole loop to decrease the processing time
#             break



def process_query(query, pipeline: QAPipeline):
    prediction = CDQA_PIPELINE.predict(query= query)
    # handle_figures(pdf_dir,pdf_scr,img_src,prediction)
    return  prediction[0]


if CDQA_PIPELINE is None:
    CDQA_PIPELINE = init_cdqa_pipeline(csv_file,model_file)

#for test
#query = "please send me the table of Word Address 1 ID Register Bit Assignments?"
#x= process_query(query, QAPipeline)
