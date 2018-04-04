#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys, os, pickle
import urllib.request
import pandas as pd
from PyPDF2 import PdfFileWriter
from PyPDF2 import PdfFileReader
from tabula import convert_into
from bs4 import BeautifulSoup

def html_mark_index(file_path):
    global m
    page = urllib.request.urlopen("file://" + file_path).read()
    soup = BeautifulSoup(page, "lxml")
    try:
        if soup.find_all(class_="me")[-1].contents[0] in "※○◎△★":
            m = soup.find_all(class_="me")
        elif soup.find_all(class_="m3")[-1].contents[0] in "※○◎△★":
            m = soup.find_all(class_="m3")
    except:
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

    m = list(filter(lambda x : x.contents[0][0] in "※○◎△★", m))
    m = m[2:]
    return m

def crop_pdf(file_path,x,y):
    input_f = PdfFileReader(open(file_path,"rb"))
    output_f = PdfFileWriter()

    numPages = input_f.getNumPages()

    sx = 39.66
    sy = y
    output_path = file_path.replace(".pdf", "_crp.pdf")
    output_path = output_path.replace("split", "crop")

    for i in range(numPages):
        page = input_f.getPage(i)
        print(page.mediaBox.getUpperRight_x(), page.mediaBox.getUpperRight_y())
        tx = page.mediaBox.getUpperRight_x()
        ty = page.mediaBox.getUpperRight_y()

        top = ty - sy - 24
        left = sx + 371

        bottom = top - 159
        right = left + 305

        page.mediaBox.loweLeft = (left,bottom)
        page.mediaBox.upperRight = (right, top)
        page.trimBox.lowerLeft = (left, bottom)
        page.trimBox.upperRight = (right, top)
        page.cropBox.lowerLeft = (left, bottom)
        page.cropBox.upperRight = (right, top)
        output_f.addPage(page)

    outputStream = open(output_path, "wb")
    output_f.write(outputStream)
    outputStream.close()
    return output_path

def convert_table(file_path):
    output_path = file_path.replace(".pdf", ".csv")
    output_path = output_path.replace("crop", "table")
    convert_into(file_path, output_path, output_format='csv')
# def html_record_index(file_path):
#     page = urllib.request.urlopen("file://" + file_path).read()
#     soup = BeautifulSoup(page, "lxml")
#     r = soup.find(string="훈련자별 입상률(%)")
#     for rr in r.find_parent("div")["class"]:
#         if 'h' in rr:
#             record_key = rr
#         else:
#             None
#     r = soup.find_all(class_=record_key)
#     return r
    # try:
    #     if soup.find_all(class_="me")[-1].contents[0] in "※○◎△★":
    #         m = soup.find_all(class_="me")
    #     elif soup.find_all(class_="m3")[-1].contents[0] in "※○◎△★":
    #         m = soup.find_all(class_="m3")
    #     else:
    #         m = soup.find_all(class_="m3")
    # except:
    #     print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    # r = soup.find_all(class_="m15")
    # for rr in r:
    #     print(rr)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print('Warning')
        sys.exit()
    src_folder = sys.argv[1]

    pd

    table_txt_path = src_folder +"/table.txt"

    with open(table_txt_path,"rb") as f:
        table_path = pickle.load(f)

    for tab in table_path:
        table_html_path =tab.replace(".pdf", ".html").replace("split", "html")
        print(html_mark_index(table_html_path))
        # html_record_index(table_html_path)
    # except:
    #     print("something is wrong")