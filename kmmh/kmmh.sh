#!/bin/sh

#1 파이썬 파일들의 맨 윗 줄에 환경 설정이 있습니다.
#  가상환경으로 돌리실 때는 이를 변경해주셔야 합니다.

#2 쉘스크립트 파일을 제외한 나머지 파이썬 파일은 kmmh 폴더 내에 위치해야합니다.
#  쉘스크립트는 어디로 이동시켜도 상관없습니다.

#3 파이썬 버전에 맞춰 다음과 같은 파이썬 모듈을 설치 해주시면 됩니다.

#pip3 install tabula
#pip3 install PyPDF2
#pip3 install selenium
#pip3 install pdfminer.six
#pip3 install bs4

#이외에도 pdf2htmlex 프로그램을 설치 하시면 됩니다

###가상환경 활성화 코드#########




##############################

#디폴트 저장소 폴더 디렉토리 
DWN_PATH=/home/korea/Downloads
#kmmh 폴더 디렉토리
KMMH_PATH=/home/korea/Desktop/kmmh

python3 $KMMH_PATH/kmmh_crawler.py $KMMH_PATH $DWN_PATH
for file in $(find ${KMMH_PATH} -type d -mindepth 1 -maxdepth 1)
$(ls -d $KMMH_PATH/*)
do
	chmod 755 ${KMMH_PATH}/log.txt | grep $file
	if [ $?='1' ];then
		python3 $KMMH_PATH/kmmh_preprocessing.py $file
		echo proprocessing done!

		python3 $KMMH_PATH/kmmh_race.py $file
		python3 $KMMH_PATH/kmmh_table.py $file
		python3 $KMMH_PATH/kmmh_log.py $file
	fi	
done

