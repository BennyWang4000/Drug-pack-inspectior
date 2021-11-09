# %%
import os
import requests
from bs4 import BeautifulSoup
import csv

base_url = 'https://www.taiwan-pharma.org.tw/public/'
# file_path = 'taiwan_pharma/'
file_path = ''
encoding = 'utf-8'


url_csv = open('detail_url.csv', newline='')
detail_csv = open(file_path + 'taiwan_pharma.csv',
                  'w', newline='', encoding="utf-8")

field_names = ['id', 'zh_drug_name', 'eng_drug_name', 'type', 'shape',
               'color', 'diameter', 'mark1', 'mark2', 'factory', 'use', 'content', 'caution', 'img_name']
csv_writer = csv.DictWriter(detail_csv, fieldnames=field_names)
csv_writer.writeheader()

# csv_writer = csv.writer(detail_csv)

# clean the csv file
fileVariable = open(file_path + 'taiwan_pharma.csv', 'r+')
fileVariable.truncate(0)
fileVariable.close()

isWatingLabel = True
label = ''

print('Finished Setup.\n')
# %%


def trim(s):
    return s.replace('\n', '').replace('\r', '').replace('\t', '').replace(' ', '')


# %%
for row in csv.reader(url_csv):
    url = base_url + row[1]
    print(url)

    response = requests.get(url)
    response.encoding = encoding
    soup = BeautifulSoup(response.text, "html.parser")

    result_table = soup.find('td', 'gb_bottom')

    row = dict()

    for td in result_table.find_all_next('td'):
        # print(trim(td.text))
        if(isWatingLabel):
            if(trim(td.text) == '許可證字號'):
                label = 'id'
                isWatingLabel = False
            elif(trim(td.text) == '中文藥名'):
                label = 'zh_drug_name'
                isWatingLabel = False
            elif(trim(td.text) == '英文藥名'):
                label = 'eng_drug_name'
                isWatingLabel = False
            elif(trim(td.text) == '劑型'):
                label = 'type'
                isWatingLabel = False
            elif(trim(td.text) == '形狀'):
                label = 'shape'
                isWatingLabel = False
            elif(trim(td.text) == '顏色'):
                label = 'color'
                isWatingLabel = False
            elif(trim(td.text) == '直徑大小'):
                label = 'diameter'
                isWatingLabel = False
            elif(trim(td.text) == '標記一'):
                label = 'mark1'
                isWatingLabel = False
            elif(trim(td.text) == '標記二'):
                label = 'mark2'
                isWatingLabel = False
            elif(trim(td.text) == '製造廠名稱'):
                label = 'factory'
                isWatingLabel = False
            elif(trim(td.text) == '臨床用途'):
                label = 'use'
                isWatingLabel = False
            elif(trim(td.text) == '成份及含量'):
                label = 'content'
                isWatingLabel = False
            elif(trim(td.text) == '注意事項'):
                label = 'caution'
                isWatingLabel = False
        else:
            row[label] = trim(td.text)
            isWatingLabel = True
    isWatingLabel = True
    print(row)
    csv_writer.writerow(row)
    row.clear

# %%
