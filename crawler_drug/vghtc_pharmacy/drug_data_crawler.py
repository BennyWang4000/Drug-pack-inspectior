# %%
# Setup:
import json
import requests
from bs4 import BeautifulSoup
import re
import csv


_ID_BASE_URL = 'http://www3.vghtc.gov.tw:8080/pharmacyHandbook/API/lookSearch.jsp'
# detail_base_url = 'http://www3.vghtc.gov.tw:8080/pharmacyHandbook/handbook.html#/data/'
_DETAIL_BASE_URL = 'http://www3.vghtc.gov.tw:8080/pharmacyHandbook/API/handbookData.jsp'
_FILE_PATH = 'data/'
_ENCODING = 'utf-8'
_CSV_FILE_NAME = 'detail.csv'
_CLEANR = re.compile('<.*?>')

id_url = ''
shape = range(1, 15)

csv_file = open(_FILE_PATH + _CSV_FILE_NAME, 'w', newline='', encoding='UTF-8')
csv_writer = csv.writer(csv_file)

header = list()
headers = set()

# clean the csv file
fileVariable = open(_FILE_PATH + _CSV_FILE_NAME, 'r+')
fileVariable.truncate(0)
fileVariable.close()


print('Finished Setup.\n')
# %%
# Function:


def flatten_json(y):
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            out[name[:-1]] = x

    flatten(y)
    return out


def cleanhtml(raw_html):
    cleantext = re.sub(_CLEANR, '', raw_html)
    return cleantext


# %%
# main:
for s in shape:
    print('\nshape: ', s)
    id_url = _ID_BASE_URL + f'?clr=0&mark=&ntch=0&shp={s}'
    # print(id_url)

    id_response = requests.get(id_url)
    id_response.encoding = _ENCODING
    id_content = json.loads(id_response.text)

    for i in id_content:
        detail_url = _DETAIL_BASE_URL + f'?code={i["UDNDRGCODE"]}'
        # print(detail_url)

        detail_response = requests.get(detail_url)
        detail_response.encoding = _ENCODING
        soup = BeautifulSoup(detail_response.text, "html.parser")

        try:
            detail = json.loads(soup.text)
        except Exception:
            print(detail_url)
            continue

        flat_detail = flatten_json(detail)
        # print(flat_detail)

        for key in flat_detail:
            if key not in headers:
                headers.add(key)
                header.append(key)

        csv_writer.writerow(cleanhtml(str(flat_detail.get(col, '')))
                            for col in header)

csv_file.close()

print('\n' + '#! Please add header manually')
print('\n', header, '\n')
print('Finished.')
# %%
