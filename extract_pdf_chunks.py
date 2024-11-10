import pdfplumber
import sys
# Example function to chunk PDF into retrievable sections


import glob
import os


def readfiles():
    os.chdir('./data')
    pdfs = []
    for file in glob.glob("*.pdf"):
        pdfs.append(file)

    return pdfs


def extract_pdf_chunks():
    myPdfs = readfiles()

    for (file) in myPdfs:
        with pdfplumber.open(file) as pdf:
            chunks = []
            print(file)
        # for page in pdf.pages:
        #     text = page.extract_text()
        #     # Splitting by double newlines as an example
        #     chunks.extend(text.split("\n\n"))
        # return chunks


sys.modules[__name__] = extract_pdf_chunks
