
import pandas as pd
import PyPDF2
import fitz
import os
import json

from os import path
from PIL import Image
from cdqa.pipeline import QAPipeline
# from preprocessing.pdfconverter import cdqa_like_df



# A Global QA_PIPELINE to be instantiated on bootstraping system
global QA_PIPELINE
QA_PIPELINE = None

dirname = path.abspath(path.dirname(__file__))

def init_QA_PIPELINE():
    """Main QA_PIPELINE intialization method, It should be called once on
    bootstraping of the system.

    @requirements:
        BERT_MODEL_PATH enviroment variable with model path
    """

    global QA_PIPELINE
    if (QA_PIPELINE == None):
        model_file = os.environ.get('BERT_MODEL_PATH', False)

        if not model_file:
            dirname = path.dirname(__file__)
            temp_file = path.join(dirname, '../models/cdqa/bert_qa.joblib')
            if not path.exists(temp_file):
                raise ">> Can't load bert model, please set BERT_MODEL_PATH env var with model path"
                return
            print('CPU Version Found')
            model_file = temp_file

        print('>>   Loading bert model..')
        qa_pipeline = QAPipeline(reader=model_file, max_df=1.0, retriever="bm25")
        print('>>   Bert Model Loaded')
        QA_PIPELINE = qa_pipeline
    return QA_PIPELINE


def process_query(query, document):
    """Main quary method that call QA_PIPELINE to predict short answer based on
    quary, and retrieve figures and table data from loaded document.

    @params:
        query: str -> user question
        document: str -> document file name to be loaded

    @return:
        response holds shortanswer, paragraph, table_data, figure_id
    """
    global QA_PIPELINE
    if (QA_PIPELINE == None):
        init_QA_PIPELINE()
    
    ALT_NAME_FILE = path.join(dirname,"../assets/lookup/protocol_names.json")
    user_doc = document
    

    
    try:
        if(str(document) == "None"):
            DOC_FILE_PDF = path.join(dirname, '../assets/pdfs/HyperBusSpecification.pdf')
            DOC_FILE_DF = path.join(dirname, '../assets/converted_documents/converted_pdfs.pickle')
        else:
            alt={}
            with open(ALT_NAME_FILE) as f:
                alt = json.load(f)
                document = alt[document]
            DOC_FILE_PDF    = path.join(dirname, '../assets/pdfs/', str(document) +".pdf")
            DOC_FILE_DF     = path.join(dirname, '../assets/converted_documents/', str(document)+".pickle")

        # df = cdqa_like_df(pd.read_pickle(DOC_FILE_DF))
        df = pd.read_pickle(DOC_FILE_DF)
        QA_PIPELINE.fit_retriever(df=df)
    
        # Make a prediction on user query
        prediction = QA_PIPELINE.predict(query=query)
    
        # Retrieve figures if any
        # TODO: TO_BE_IMPLEMENTED Retrieve prediction page number to avoid looping through all pdf file pages
        DOC_PAGE_NUM_OF_PREDICTION = 0
        figure_id = handle_figures(DOC_FILE_PDF, prediction=prediction, page_number=DOC_PAGE_NUM_OF_PREDICTION)
    
        # Retrieve table data if any
        # TODO: TO_BE_IMPLEMENTED Retrieve table data from prediction object if ant
        table_data = None
    
    
        # Generate response data
        # TODO: TO_BE_IMPLEMENTED append figures and table data to response, change response to JSON format
        response = prediction[0]
        if prediction[2]:
            response = f'{prediction[0]} \n\n paragraph: \n {prediction[2]}'
        return response
    except Exception as e:
        print(2, e)
        return f'There is no protocol called {user_doc} \n Please specify the right name of the protocol in your question. \n\n Ex: What is RWDS in HyperBusSpecification protocol?'

    # Retrieve Data of PDF and fit model
    # TODO: 1. TO_BE_IMPLEMENTED load specific file using extracted document name from question
    # TODO: 2. After loading file use [cdqa_like_df] from preprocessing.pdfconverter and pass loaded object to it to convert data frame to cdqa df
        # TODO: 2. _EXPLANATION_ pickles files are an object of PDFParser not an pandas dataframe
        # TODO: 2. _EXPLANATION_ our object has df with ['paragraghs', 'tables'], and cdqa requires df with ['title', 'paragraphs']
    



def handle_figures(pdf_scr, prediction, page_number=None):
    """Main figures handler method it search for prediction short answer inside
    pdf file and highlight it.

    @params:
        pdf_scr: str -> pdf file path to search inside
        prediction: object -> QA_PIPELINE prediction object

    @return:
        figure id saved in assets/imgs/{fig_id}.png
    """

    # TODO: TO_BE_IMPLEMENTED[After process_query function TODO] delete looping through all pages and use page_number argument for more efficiency
    # TODO: TO_BE_IMPLEMENTED[After process_query function TODO] delete looping through all pages and use page_number argument for more efficiency

    # TODO: TO_BE_IMPLEMENTED create a temp file for each image [we shouldn't delete images to be able to display them in client side]
    FIG_ID = 'out'
    FIG_TEMP_FILE = path.join(dirname, f'../assets/imgs/{FIG_ID}.png')

    # creating a pdf file object
    pdfFileObj = open(pdf_scr, 'rb')

    # creating a pdf reader object
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    para = prediction[2]

    # creating a page object
    for page in range(pdfReader.numPages):
        # creating rotated page object
        pageObj = pdfReader.getPage(page)
        txt= pageObj.extractText()
        txt2 =txt.replace('\n', '')

         #check to return the image
        if(txt2.find(para)!=-1 and (para.split(None, 1)[0] == "Figure" or para.split(None, 1)[0] == "Table")):

            # code for highlighting the figures and produce the image
            doc = fitz.open(pdf_scr)
            page2 = doc[page]
            #print(page2)
            text_instances = page2.searchFor(para)
            #print(text_instances)

            # HIGHLIGHT
            for inst in text_instances:
                highlight = page2.addHighlightAnnot(inst)

            ### OUTPUT IMAGE
            pix = page2.getPixmap()
            out = "out.png"
            pix.writePNG(FIG_TEMP_FILE)
            img = Image.open(FIG_TEMP_FILE)
            img.show()

            #break from the whole loop to decrease the processing time
            break

    return FIG_ID
