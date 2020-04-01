from tika import parser

import pandas as pd
import numpy as np
import nltk
import camelot
import random
import re



# import pprint


# pp = pprint.PrettyPrinter(indent=4)



class BaseParser(object):

    def parse(self):
        pass

    def save(self, file_path):
        pass



class PDFParser(BaseParser):

    _pdfPath = None
    _data = pd.DataFrame(columns=['paragraghs', 'tables'])

    def __init__(self, pdfPath):
        super().__init__()
        self._pdfPath = pdfPath
        self.parse()


    def parse(self):
        pages = self.parseTika()
        for index, page in enumerate(pages):
            tables = self.parseCamelot(index+1)
            if tables:
                self._data = self._data.append(self._parsePage(page, tables), ignore_index=True)
            else:
                self._data = self._data.append(self._textToParagraphs(page), ignore_index=True)


    def _parsePage(self, page, tables):
        pretext = page

        processed = pd.DataFrame(columns=['paragraghs', 'tables'])

        for table in tables:
            df = table.df
            headers = df.iloc[0]
            df = df[1:]
            df.columns = headers
            df = df.replace('', np.nan)
            df = df.ffill(axis=0)
            shape = df.shape

            try:
                start = re.escape(str(df.iloc[0,0])).replace("\\\n","(\ |\\n)*")
                end = re.escape(str(df.iloc[-1,-1])).replace("\\\n","(\ |\\n)*")

                regex_content = f"(({start})(.|\\n)*?({end}))"
                regex = re.compile(regex_content)

                search = regex.search(pretext) 
                start = search.start()
                end = search.end()

                processed = processed.append( self._textToParagraphs(pretext[:start-1]), ignore_index=True)
                processed = processed.append( {'paragraghs': self.tableDFtoParagraph(df), 'tables': table.df.to_html()}, ignore_index=True)
                pretext = pretext[end:]

            except Exception as e:
                print(str(e))
        return processed


    def _textToParagraphs(self, text):
        df = pd.DataFrame(columns=['paragraghs', 'tables'])
        pgs = re.split(r'(?:\r?\n){2,}', text)
        for pg in pgs:
            df = df.append({'paragraghs': pg.strip(), 'tables': None}, ignore_index=True)
        return df


    def parseTika(self):
        if not self._pdfPath:
            raise 'Please Provide a path to PDF file'

        response = parser.from_file(self._pdfPath, xmlContent=True)
        xmlBody = response['content'].split('<body>')[1].split('</body>')[0]
        xmlBody = xmlBody.replace("<p>", "").replace("</p>", "").replace("<div>", "").replace("</div>","").replace("<p />","")
        xmlBody = xmlBody.split("""<div class="page">""")[1:]
        return xmlBody

    
    def parseCamelot(self, pageNo):
        if not (type(pageNo) == str):
            pageNo = f'{pageNo}'

        return camelot.read_pdf(self._pdfPath, flavor='lattice', pages=f'{pageNo}', suppress_stdout = True)


    def tableDFtoParagraph(self, df):
        text = ''
        for index, row in df.iterrows():
            row = row.to_dict()
            for key, value in row.items():
                key = str(key)
                value = str(value)
                text += key.replace('\n', ' ').strip() + ': ' + value.replace('\n', ' ').strip() + ', '
            text = text[0: -2]
            text += '\n'
        text.strip()
        return text


    def getData(self):
        return self._data