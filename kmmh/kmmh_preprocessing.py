#!/usr/bin/env python
#-*- coding: utf-8 -*-

from PyPDF2 import PdfFileWriter, PdfFileReader
from tabula import read_pdf
import os, sys, pickle
import subprocess

def split_pdf(file_path):
    folder_path = os.path.dirname(file_path)
    split_path = folder_path + '/split'
    if not os.path.isdir(split_path):
        os.mkdir(split_path)
    input_pdf = PdfFileReader(open(file_path, "rb"))
    file_path_list = []
    for i in range(input_pdf.numPages):
        output = PdfFileWriter()
        output.addPage(input_pdf.getPage(i))
        out_path = file_path.replace(".pdf", "_p%s.pdf" % (i + 1))
        out_path = out_path.replace(folder_path, split_path)
        file_path_list.append(out_path)
        with open(out_path, "wb") as outputStream:
            output.write(outputStream)
    print("cropping finished")
    return file_path_list

def validate_page_list(file_path):
    data = read_pdf(file_path, output_format="json")
    file_urls = [None, None]
    for d in data:
        for dd in d['data']:
            for ddd in dd:
                if "경기마별산성나" not in ddd["text"]:
                    pass
                else:
                    try:
                        file_urls[0] = file_path
                    except:
                        print("vaLue error : No specific word or Key value")
    for d in data:
        for dd in d['data']:
            for ddd in dd:
                if "⩘が" not in ddd["text"]:
                    pass
                else:
                    try:
                        file_urls[1] = file_path
                    except:
                        print("vaLue error : No specific word or Key value")
    return file_urls

def create_db(folder_path):
    db_path = folder_path+'/db'
    if not os.path.isdir(db_path):
        os.mkdir(db_path)

def convert_html(file_path, output_folder_path):
    subprocess.call(["pdf2htmlEX","--dest-dir",output_folder_path, file_path], shell=False)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print('Warning')
        sys.exit()
    dir_path = sys.argv[1]
    try:
        files = os.listdir(dir_path)
        for f in files:
            if ".pdf" in f:
                src_file = dir_path + "/" + f
        split_list = split_pdf(src_file)
        race_path =[]
        table_path =[]
        for spl in split_list:
            val = validate_page_list(spl)
            if val[0] != None:
                table_path.append(spl)
            else:
                continue
            # 경기 예측 페이지 추출
            if val[1] != None:
                race_path.append(spl)
            else:
                continue
        html_path = dir_path +"/html"
        for html in race_path + table_path:
            convert_html(html, html_path)

        create_db(dir_path)
        race_file = dir_path + "/race.txt"
        table_file = dir_path + "/table.txt"

        with open(race_file,'wb') as f:
            pickle.dump(race_path,f)
        f.close()

        with open(table_file,'wb') as f:
            pickle.dump(table_path,f)
        f.close()
    except:
        None
