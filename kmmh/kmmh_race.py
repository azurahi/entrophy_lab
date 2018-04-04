#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os, re, shutil, sys,pickle
import csv
# Import external packages
import pdfminer
from pandas import DataFrame
import pandas as pd

from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage, PDFTextExtractionNotAllowed
from pdfminer.pdfparser import PDFParser
from bs4 import BeautifulSoup
import urllib.request
from urllib import request

# from constGlobal import *

AREA_EVAL_RELEVANCE = (0, 150, 800, 1050)
AREA_RACESUMMARY = (0, 737, 0, 1050)
AREA_RACENAME = (50, 300, 1000, 1200)
AREA_OF_INTEREST_0 = (150, 300, 900, 1020) # [165.84, 985.02, 271.919, 1009.338]
area_habbit = (150, 300, 750, 850) # 질주습성
area_habbit2 = (150, 300, 750, 870)
area_prediction = (550, 737, 750, 1020)


SEQ_RUNTYPE = ["추입","선입","자유","선행","도주"] # Reversed form the order of occurence for indexing
SEQ_CHAR_NUM_CIRCLE = ["①","②","③","④","⑤","⑥","⑦","⑧","⑨","⑩","⑪","⑫","⑬","⑭"]
CHAR_STAR = "★"

def render_data_racename(textbox_cropped):
    ret = []
    for textbox in textbox_cropped:
        textbox_rendered = textbox["text"]
        textbox_rendered = textbox_rendered.replace(" ","")
        ret.append(textbox_rendered[:2])
        ret.append(textbox_rendered[2])
    return ret

def extract_layout_by_page(pdf_path):
    laparams = LAParams()

    fpath = open(pdf_path, 'rb')
    parser = PDFParser(fpath)
    document = PDFDocument(parser)

    if not document.is_extractable:
        raise PDFTextExtractionNotAllowed

    rsrcmgr = PDFResourceManager()
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)

    layouts = []
    for page in PDFPage.create_pages(document):
        interpreter.process_page(page)
        layouts.append(device.get_result())

    return layouts

def is_inside(coord_input, coord_area): # Left Right Bottom Top
    if coord_input[0] > coord_area[0] and coord_input[1] < coord_area[1] and coord_input[2] > coord_area[2] and coord_input[3] < coord_area[3]:
        return True
    else:
        return False

def get_seq_textbox(page_layout):
    seq_textbox = []
    for cell in page_layout:
        try:
            textbox = {}
            textbox['text'] = cell.get_text()
            textbox['coord'] = (cell.x0, cell.x1, cell.y0, cell.y1) # Left Right Bottom Top
            seq_textbox.append(textbox)
        except AttributeError:
            pass
    return seq_textbox

def crop_area(seq_textbox, area):
    textbox_cropped = []
    for textbox in seq_textbox:
        if is_inside(textbox['coord'], area):
            textbox_cropped.append(textbox)
    return textbox_cropped
# 			elem_rem = text.decode('utf-8').encode('utf-8')
# 			elem_rem = re.sub(r"\s", r"", text)

def get_seq_textbox_cropped(fpath, area_cropped):
	page_layout = extract_layout_by_page(fpath)[0] # We only deal with a single page
	seq_textbox = get_seq_textbox(page_layout)
	seq_textbox_cropped = crop_area(seq_textbox, area_cropped)
	return seq_textbox_cropped

def render_data_AOI2(textbox_cropped):
    seq_textbox_rendered = []
    for textbox in textbox_cropped:
        # rec_name = ""
        # for x in re.findall(r"\(.*?\)", textbox["text"]):
        # 	rec_name = rec_name + x + " "

        rec_ranking = ""
        # print(textbox["text"])
        for x in re.findall(r"\s\d+", textbox["text"]):
            rec_ranking = rec_ranking + x.strip() + ", "
        # textbox_rendered = rec_ranking.rstrip(", ")#rec_name + ", " + rec_ranking.rstrip(", ")
        # seq_textbox_rendered.append(textbox_rendered)
        seq_textbox_rendered.append(str(rec_ranking.rstrip(", ")))
    return seq_textbox_rendered

def make_str_fwrite_AOI2(fpath, seq_textbox_rendered):
    str_fwrite = ""
    for textbox_rendered in seq_textbox_rendered:
        if len(textbox_rendered.split(",")) == 6:
            str_fwrite = str_fwrite + fpath + ", " + textbox_rendered + "\n"
    return str_fwrite

def render_data_AOI1(textbox_cropped):
    top = None
    bottom = None
    for textbox in textbox_cropped:
        text = str(textbox["text"])
        if "도주" in text:
            top, bottom = textbox["coord"][3], textbox["coord"][2]
    # print(top, bottom)
    height_cell = (top - bottom) / 5

    seq_textbox_rendered = []
    for textbox in textbox_cropped:
        # Clean case
        if textbox["coord"][3] - textbox["coord"][2] < 15:
            str_horse = textbox["text"]
            padding = int((textbox["coord"][2] - bottom) // height_cell)

            seq_textbox_rendered.append([padding, str_horse])
        # Nasty case
        elif textbox["coord"][3] - textbox["coord"][2] < 30:
            seq_line = str(textbox["text"]).split("\n")[:-1]
            seq_line.reverse()

            for i, line in enumerate(seq_line):
                str_horse = line
                padding = int((textbox["coord"][2] + i * height_cell - bottom) // height_cell)
                seq_textbox_rendered.append([padding, str_horse])
    ret = []
    for textbox_rendered in seq_textbox_rendered:
        if 0 <= textbox_rendered[0] and textbox_rendered[0] < 5:
            ret.append([SEQ_RUNTYPE[textbox_rendered[0]], textbox_rendered[1]])
    return ret

def make_str_fwrite_AOI1(fpath, seq_textbox_rendered):
    str_fwrite = ""
    for textbox_rendered in seq_textbox_rendered:
        str_fwrite = str_fwrite + fpath + ", " + textbox_rendered[0] + ", " + textbox_rendered[1].rstrip() + "\n"
    str_fwrite.rstrip("\n")
    return str_fwrite

def get_seq_textbox_cropped(fpath, area_cropped1, area_cropped2, area_cropped3):
    page_layout = extract_layout_by_page(fpath)[0] # We only deal with a single page
    seq_textbox = get_seq_textbox(page_layout)
    seq_textbox_cropped1 = crop_area(seq_textbox, area_cropped1)
    seq_textbox_cropped2 = crop_area(seq_textbox, area_cropped2)
    seq_textbox_cropped3 = crop_area(seq_textbox, area_cropped3)
    return seq_textbox_cropped1, seq_textbox_cropped2, seq_textbox_cropped3

def html_index(file_path):
    name_list = []
    rank_list = []
    mark_list = []
    page = urllib.request.urlopen("file://" + file_path).read()
    soup = BeautifulSoup(page, "lxml")
    # t = soup.find(string="우승확률")
    # if t != None:
    #     tt = t.find_parent("div")["class"]
    #     for ttt in tt:
    #         if 'm' in ttt:
    #             name_key = ttt
    #         else:
    #             None
    #
    #     names = soup.find_all(class_=name_key)
    #     for t in names[-5:]:
    #         name_list.append(t.string)
    #
    #     z = names[-5]
    #     zz = z.previous_sibling["class"]
    #     for zzz in zz:
    #         if 'ff' in zzz:
    #             rank_key = zzz
    #         else:
    #             None
    #     marks = soup.find_all(class_=rank_key)
    #     for z in marks[:5]:
    #         rank_list.append(z.string)
    #
    #     q = soup.find_all(class_="m4")
    #     for qq in q[-2:]:
    #         for qqq in qq.string:
    #             mark_list.append(qqq)
    # else:
    state = soup.find(string='ॴྡྷ').find_parent("div")["class"]
    for s in state:
        if 'm' in s:
            key = s
    q = soup.find_all(class_=key)
    for qq in q[::-1]:
        if len(qq.string) ==2:
            q_n = q.index(qq)
            break
    for qq in q[q_n-1:q_n+1]:
        for qqq in qq.string:
            mark_list.append(qqq)

    zz = q[q_n].next_sibling["class"]
    for zzz in zz:
        if 'ff' in zzz:
            rank_key = zzz
        else:
            None
    marks = soup.find_all(class_=rank_key)
    for z in marks[:5]:
        rank_list.append(z.string)
    tt = marks[0].next_sibling["class"]
    for ttt in tt:
        if 'm' in ttt:
            name_key = ttt
        else:
            None

    names = soup.find_all(class_=name_key)
    for t in names[-5:]:
        name_list.append(t.string)

    return(name_list, rank_list, mark_list)

def html_namer(file_path):
    name_code = {'তᠵఌ': '김병남', '⃵๤⋜': '양대인', '⋘ㆸ᎝': '이화령', '⍹エᡭ': '정필봉', '⍹↨ࢴ': '정완교', 'ᲀᲁ㈬': '서석훈', '⋘Ⅵↈ': '이영오',
                 'ᲁ㆜エ': '석호필', 'Ṑ㆜ॠ': '심호근', '⋘⠑⹰': '이청파', 'ᘌᰥ㆜': '모상호', '⊄⑤ᰥ': '유준상', '⏩Ύネ': '종합'}
    name_list = []
    page = urllib.request.urlopen("file://" + file_path).read()
    soup = BeautifulSoup(page, "lxml")
    tot = soup.finm
    tt = tot.find_parent("div").previous_sibling.previous_sibling.previous_sibling["class"]
    for ttt in tt:
        if 'm' in ttt:
            name_key = ttt
        else:
            None
    names = soup.find_all(class_=name_key)
    for n in names:
        name = n.string
        try:
            name_list.append(name_code[name])
        except:
            name_list.append("불명")

    name_list.append("종합")

    return name_list
    #     if soup.find_all(class_="me")[-1].contents[0] in "※○◎△★":
    #         m = soup.find_all(class_="me")
    #     elif soup.find_all(class_="m3")[-1].contents[0] in "※○◎△★":
    #         m = soup.find_all(class_="m3")
    #     else:
    #         m = soup.find_all(class_="m3")
    # except:
    #     print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    r = soup.find_all(class_="m15")
    for rr in r:
        print(rr)



if __name__ == "__main__":
    if len(sys.argv) != 2:
        print('Warning')
        sys.exit()
    src_folder = sys.argv[1]

    race_txt_path = src_folder +"/race.txt"

    with open(race_txt_path,"rb") as f:
        race_path = pickle.load(f)
    # print(race_path)

    df = DataFrame(columns=("경기명","경기번호","도주","선행","자유","선입","추입","전문가","전문가예측","메인예측_경기마","메인예측_경기순위","메인예측_경기표식"))

    for race in race_path:
        #경기명 추출
        seq_textbox_cropped = get_seq_textbox_cropped(race, AREA_RACENAME, area_habbit2, area_prediction)
        seq_textbox_rendered = render_data_racename(seq_textbox_cropped[0])
        game_place = seq_textbox_rendered[0]
        game_number = seq_textbox_rendered[1]
        #질주습성
        habbit = ['','','','','']
        habbit_rendered = render_data_AOI1(seq_textbox_cropped[1])
        for hab in habbit_rendered:
            hab[1] = hab[1].strip()

            if hab[0] in "도주":
                habbit[0] = hab[1]
            elif hab[0] in "선행":
                habbit[1] = hab[1]
            elif hab[0] in "자유":
                habbit[2] = hab[1]
            elif hab[0] in "선입":
                habbit[3] = hab[1]
            elif hab[0] in "추입":
                habbit[4] = hab[1]

        #전문가 예측(예측번호만)
        predication_rendered = render_data_AOI2(seq_textbox_cropped[2])
        ####################################################################
        race_html_path=race.replace(".pdf",".html").replace("split","html")
        #메인 경기 내용 추출
        game_predict = html_index(race_html_path)
        prediction_name = html_namer(race_html_path)

        df = df.append([game_place, game_number,habbit[0],habbit[1],habbit[2],habbit[3],habbit[4],prediction_name,predication_rendered[0],game_predict[0],game_predict[1],game_predict[2]])
        print('processing')

    df.to_csv(path_or_buf=src_folder+'/db/race.csv')

