import os
import pandas as pd
from ast import literal_eval

from cdqa.utils.converters import pdf_converter
from cdqa.utils.filters import filter_paragraphs
from cdqa.pipeline import QAPipeline
from cdqa.utils.download import download_model



df = pdf_converter(directory_path='./data/pdf/')
#df.head()
df.to_csv(r'D:\gp\cdQA testing\data_pdf\csv\converted_pdfs.csv', index = False)
