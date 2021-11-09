# %%
# Setup
from json import decoder
import urllib.request
import csv

_BASE_URL = 'http://www3.vghtc.gov.tw:8080/pharmacyHandbook/API/getImage.jsp?path=pic&code='
_CSV_FILE_PATH = 'data/'
_CSV_FILE_NAME = 'detail.csv'
_IMG_FILE_PATH = 'img/'

csv_file = open(_CSV_FILE_PATH + _CSV_FILE_NAME, "r",  encoding='utf-8')
csv_reader = csv.DictReader(csv_file)

print('Finished Setup.')
# %%
# main

#
for lines in csv_reader:
    # print(lines.keys())
    code = lines[" 'UDNDRGCODE'"]
    try:
        urllib.request.urlretrieve(
            _BASE_URL + code, _IMG_FILE_PATH + code + '.jfif')
    except Exception:
        print(code)

print('main finished.')

# %%
