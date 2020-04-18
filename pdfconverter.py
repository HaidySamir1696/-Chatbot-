from argparse import ArgumentParser
import pandas as pd
import pickle

from core import PDFParser

def convert_to_df(filepath):
    pdfParser = PDFParser(filepath, include_line_breaks=False)

    paragraphs = pdfParser.getData().loc[:,'paragraghs'].to_numpy()
    df = pd.DataFrame(columns=["title", "paragraphs"])
    df = df.append({'title': 'HyperBus', 'paragraphs':paragraphs}, ignore_index=True)
    return df


if __name__ == "__main__":
    parser = ArgumentParser(description="PDF documents converter")
    parser.add_argument('-file', help='PDF document path to convert')
    parser.add_argument('-cache', help='File path to cache conversion process')

    args = parser.parse_args()

    filepath = args.file
    cachefilepath = args.cache

    print('PDF Parser >> Start Parsing PDF File')
    df = convert_to_df(filepath)

    print(f'PDF Parser >> Saving to {cachefilepath}')
    with open(cachefilepath, 'wb') as f:
        pickle.dump(df, f)
    print(f'PDF Parser >> Done')