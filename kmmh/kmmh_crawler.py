#!/usr/bin/env python
#-*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

import shutil, os, time, sys
import pickle
import urllib.request

def file_crawler(dir_path, dwn_path, start_num):
    try:
        with open(dir_path+'/list.txt','rb') as f:
            download_list = pickle.load(f)
            end_num = download_list[-1]
            print(end_num)
    except:
        download_list = []
        end_num = 0
        print("Initializing")

    driver = webdriver.Chrome(dir_path+"/chromedriver") #크롬켜기

    driver.get('http://www.krj.co.kr/mainBody.phtml') #경마문화 사이트 접속
    #mainBody.phtml에 씌워져있는 것이므로 여기까지 url을 잡아줘야한다.

    ###아이디 비밀번호###
    krj_id = 'fadala'
    krj_pw = 'fadala203'
    ####################

    #아이디 비밀번호 입력
    driver.find_element_by_name('userid').send_keys(krj_id)
    driver.find_element_by_name('password').send_keys(krj_pw)

    #로그인 버튼 눌러주기
    driver.find_element_by_name('image').click()

    #다운로드 페이지 이동
    down_url = 'http://www.krj.co.kr/ebook/ecatalog5.php?catimage=1&Dir=' #228페이지부터 1페이지까지존재한다.

    #일정기간에 한번씩 range업데이트 필요
    for i in range(start_num, end_num, -1):
        down_url_full = down_url + str(i)
        driver.get(down_url_full)
        try:
            driver.find_element_by_id('downsect').click()
        except:
            pass
        time.sleep(1)


    #일정시간동안 대기 하기
    time.sleep(10)

    #download file 옮기기
    file_list = os.listdir(dwn_path) #하위 디렉토리 파일 리스트로 반환
    file_list.sort() #정렬

    for file in file_list:
        if file.find('catImage') is not -1:
            try:
                if file.find('R') is not -1:
                    index1 = file.find('R')
                    index2 = file[1:].find('-') + 1
                    date = file[index1 + 1:index1 + 9]
                    num = file[index2 + 1:index1 - 1]
                else:
                    index1 = file.find('20')
                    index2 = file[1:].find('-') + 1
                    date = file[index1:index1 + 8]
                    num = file[index2 + 1:index1 - 1]
            except:
                print("bad file exists")

            # item = file[11:].replace("-", "  -")
            # if int(item[0:3]) < 10:
            #     folder_name = item[5:13]
            #     num_name = item[0:3]
            # elif int(item[0:3]) < 100:
            #     folder_name = item[6:14]
            #     num_name = item[0:3]
            # elif int(item[0:3]) < 1000:
            #     folder_name = item[7:15]
            #     num_name = item[0:3]
            new_dir_path = dir_path + '/' + date
            if not os.path.isdir(new_dir_path):
                os.mkdir(new_dir_path)
            new_name = new_dir_path + '/' +"kmmh-" + num + "-R" + date +".pdf"
            shutil.move(dwn_path +'/'+ file, new_dir_path + '/' + file) #찾은 것을 옮길 디렉토리로 옮기기
            os.rename(new_dir_path + '/' + file, new_name)

            download_list.append(num)

    download_list.sort()
    with open(dir_path + '/list.txt','wb') as f:
        pickle.dump(download_list,f)
    f.close()
    print("complete")


def new_file_checker(dir_path):
    with open(dir_path + '/' + 'list.txt', 'r') as f:
        try:
            data = pickle.load(f)
        except:
            data = [228]
        num = data[-1]+1
        while 'window.alert' not in str(urllib.request.urlopen('http://www.krj.co.kr/ebook/ecatalog5.php?catimage=1&Dir=%d'%num).read()):
            num += 1
        num -= 1
        if num != data[-1]+1:
            return num
        else:
            return False

if __name__== "__main__":
    if len(sys.argv) != 3:
        print('Warning')
        sys.exit()
    dir_path = sys.argv[1]
    dwn_path = sys.argv[2]
    if new_file_checker(dir_path) is not False:
        file_crawler(dir_path,dwn_path, new_file_checker(dir_path))
    else:
        print("No Need to Update")