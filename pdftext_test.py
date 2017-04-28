# -*- coding: utf-8 -*-
"""
Created on Mon Apr 10 09:25:01 2017

@author: justi
"""

import PyPDF2
from transformtext import TransformText

pdfFileObj = open('Crop Listing.pdf', 'rb')
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

num = pdfReader.numPages
page = []



count = 0
while count < num:
    pageObj = pdfReader.getPage(count)
    x = pageObj.extractText()

    p = TransformText(x)
    c_response = p.clean_html(p.t_text) #remove any unwanted markup in a given text response

    page.append(c_response)

    sents = p.get_sentences()
    words = p.space_tagger(c_response) #calle the spacy.io POS Tagging method
    parsed_words = p.parse(words) #create np chunks

    p.np_sub_chunks(parsed_words)
    ents = p.return_sub_chunks(lower=False)
    print("printing: page - ", x)
    print("printing phrases: ", p.sent_phrases)
    print("printing sents: ", sents)

    count = count+1
