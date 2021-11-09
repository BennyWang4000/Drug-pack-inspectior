# %%
import os
import requests
from bs4 import BeautifulSoup
import csv

url = 'https://www.taiwan-pharma.org.tw/public/public_search.php'
encoding = 'utf-8'
csv_file_name = 'url_Round_Flat.csv'

parameters = ['DrugName', 'DetailUrl']
csv_file = open(csv_file_name, 'w', newline='')
field_names = ['DrugName', 'DetailUrl']
csv_writer = csv.DictWriter(csv_file, fieldnames=field_names)
csv_writer.writeheader()

# clean the csv file
fileVariable = open('detail_url.csv', 'r+')
fileVariable.truncate(0)
fileVariable.close()

print('Finished Setup.\n')
# %%


for i in range(286):
    parameters['page'] = i + 1
    r = requests.Session()
    response = r.post(url, data=parameters)
    response.encoding = encoding
    soup = BeautifulSoup(response.text, "html.parser")

    result_table = soup.find('table', 'bottomline_gray')

    for row in result_table.find_all('tr')[1:]:
        drug_name_field = row.find_all('td')[1]
        drug_name = drug_name_field.text
        detail_url_field = row.find_all('a', href=True)[0]
        detail_url = detail_url_field['href'].split("'")[1]
        print(drug_name)
        print(detail_url)

        csv_writer.writerow({'DrugName': drug_name,
                            'DetailUrl': detail_url})

print('\n', 'Finished.')


# response = requests.get(url)
# response.encoding = encoding
# soup = BeautifulSoup(response.text, "html.parser")


# for a in result_table.find_all('a', href=True):
#     print(a['href'], '\n')

# print(response.text)

# html = soup.prettify()
# print(html)
# # %%
# with open("out.txt", "w") as out:
#     for i in range(0, len(html)):
#         try:
#             out.write(html[i])
#         except Exception:
#             pass

# # %%

# %%
