from tika import parser

import pandas as pd
import numpy as np
import camelot
import random
import re

class BaseParser(object):

    def parse(self):
        pass

    def save(self, file_path):
        pass



class PDFParser(BaseParser):

    _pdfPath = None
    _name = ''
    _data = pd.DataFrame(columns=['paragraghs', 'tables'])
    _htmlTables = []

    _include_line_breaks = False

    def __init__(self, pdfPath, filename, include_line_breaks=False):
        super().__init__()
        self._name = filename
        self._include_line_breaks = include_line_breaks
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
            self._htmlTables.append(table.df.to_html())
            tableindex = len(self._htmlTables) -1

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

                pgs = self.tableDFtoParagraph(df)
                pgs = re.split(r'(?:\r?\n){2,}', pgs)

                for pg in pgs:
                    processed = processed.append( {'paragraghs': pg, 'tables': tableindex}, ignore_index=True)


                pretext = pretext[end:]

            except Exception as e:
                print(1, str(e))
        try:
            processed = processed.append( self._textToParagraphs(pretext), ignore_index=True)
        except Exception as e:
            print(0, str(e))
        return processed


    def _textToParagraphs(self, text, min_length=200):
        df = pd.DataFrame(columns=['paragraghs', 'tables'])
        pgs = re.split(r'(?:\r?\n){2,}', text.strip())

        temp_para = ''
        for pg in pgs:
            if pg.isspace():
                if temp_para:
                    df = df.append({'paragraghs': temp_para.strip(), 'tables': None}, ignore_index=True)
                continue

            if self._include_line_breaks:
                if len(pg) >= min_length:
                    if temp_para:
                        df = df.append({'paragraghs': temp_para.strip(), 'tables': None}, ignore_index=True)
                        temp_para = ""
                        df = df.append({'paragraghs': pg.replace("\n", "").strip(), 'tables': None}, ignore_index=True)
                    else:
                        df = df.append({'paragraghs': pg.replace("\n", "").strip(), 'tables': None}, ignore_index=True)
                else:
                    line = pg.replace("\n", " ").strip()
                    temp_para = temp_para + f" {line}"
            else:
                df = df.append({'paragraghs': pg.replace("\n", "").strip(), 'tables': None}, ignore_index=True)

        return df


    def parseTika(self):
        if not self._pdfPath:
            raise 'Please Provide a path to PDF file'

        response = parser.from_file(self._pdfPath, xmlContent=True)
        if not response['content']:
            raise '>> Error while parsing using Tika, No content available in tika response.'
            return 
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
                text += key.replace('\n', ' ').strip() + ': ' + "'" + value.replace('\n', ' ').strip() + "'" + ', '
            text = text[0: -2]
            text += '\n\n'
        text = text.strip()
        return text


    def getData(self):
        return self._data

    def getHTMLTable(self, index):
        return self._htmlTables[index]

    def getFileName(self):
        return self._name