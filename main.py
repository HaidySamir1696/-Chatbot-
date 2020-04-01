

from parser.pdfparser import PDFParser


filepath = './data/HyperBusSpecification.pdf'

pdfParser = PDFParser(filepath)

df = pdfParser.getData()
