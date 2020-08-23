import pandas as pd
import pickle

from os import path

from preprocessing.parser import PDFParser

dirname = path.abspath(path.dirname(__file__))


def cdqa_like_df(pdfparser_obj):
    """
        Return a data frame with ['title', 'paragraphs'] like required by cdqa

        @params:
            pdfparser_obj: PDFParser -> an 'PDFParser' object to retrieve data of document
    """
    paragraphs = pdfparser_obj.getData().loc[:,'paragraghs'].to_numpy()
    title = pdfparser_obj.getFileName()

    df = pd.DataFrame(columns=["title", "paragraphs"])
    df = df.append({'title': title, 'paragraphs':paragraphs}, ignore_index=True)
    return df


def convert_pdf(file_path, filename, include_line_breaks=False) -> PDFParser:
    """
        Start process convertion and return an PDFParser object

        @params:
            file_path: str -> PDF file path to parse
            include_line_breaks: bool -> if true PDFParser will merge small paragraphs together
    """
    return PDFParser(file_path, filename=filename, include_line_breaks=include_line_breaks)


def parse_pdf_and_save(file_path, dest_path, doc_name, include_line_breaks=False):
    """
        Parse PDF and save cache of convertion process in an Pickle file

        @params:
            file_path: str -> PDF file path to parse
            dest_path: str -> directory path to save cache file
            name: str -> name of document to save cache with
            include_line_breaks: bool -> if true PDFParser will merge small paragraphs together
    """
    doc_name = doc_name.strip()
    name_ext = ''

    if path.isfile(dest_path):
        raise "Destination path should be a directory to store convertion process not a file."

    if doc_name.endswith('.pickle'):
        doc_name = doc_name.replace('.pickle', '')
        name_ext = doc_name + '.pickle'
    else:
        name_ext = doc_name + '.pickle'

    dest_path = path.join(dest_path, name_ext)

    if path.exists(dest_path):
        raise "This file name exists before please delete the old version first"
    
    pdfParser = convert_pdf(file_path, filename=doc_name, include_line_breaks=include_line_breaks)

    with open(dest_path, 'wb') as f:
        pickle.dump(pdfParser, f)

    return pdfParser