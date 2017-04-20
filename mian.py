
__author__ = 'mattmilliken'

from pdfminer.pdfparser import PDFParser, PDFObjRef
import os
from pdfminer.pdfdocument import PDFDocument

from time import mktime, strptime

from datetime import datetime

import sqlalchemy

#Create the Folder LWB Issues

directory = "LWB Issues"
if not os.path.exists(directory):
    os.makedirs(directory)


# fp = open('ISSUE-596-WEB.pdf', 'rb')
#
# parser = PDFParser(fp)
#
# doc = PDFDocument(parser)
#
# datestring = doc.info[0]['CreationDate'][2:-7]
# datestring = datestring.decode('utf-8')
#
# ts = strptime(datestring, "%Y%m%d%H%M%S")
#
# dt = datetime.fromtimestamp(mktime(ts))
#
#
# print(dt)

from urllib.request import urlopen


def download_file(file_url, file_out):
    response = urlopen(file_url)

    file = open(file_out, 'wb')

    file.write(response.read())
    
    file.close()

    print("complete")

# download_file("https://media.readthedocs.org/pdf/pdfminer-docs/latest/pdfminer-docs.pdf")




from bs4 import BeautifulSoup

BASE_URL = "https://lwb.co.nz/issue-archive/?start="
START_URL_ID = 0
START_URL_INCREMENT = 20
START_URL_FINAL = 160



# while START_URL_ID <= START_URL_FINAL:
#
#     r = urlopen(BASE_URL + str(START_URL_ID))
#
#     soup = BeautifulSoup(r)
#     soup.prettify()
#     issues = (soup.find_all("div", class_="mainContent ArchiveWidget"))
#
#
#
#     for i in issues:
#         for link in i.find_all('a', href=True):
#             print(link['href'])
#
#         for issueNum in i.find_all("a", class_="dotted"):
#             print(issueNum.text)
#
#         for date in i.find_all("p", class_="date"):
#             print(date.text)
#
#
#     START_URL_ID += START_URL_INCREMENT
#
#
#
#
#
r = urlopen(BASE_URL + str(START_URL_ID))
import re
soup = BeautifulSoup(r)
soup.prettify()
issues = (soup.find_all("div", class_="mainContent ArchiveWidget"))

issueArray = []



for li in issues[0].find_all("li"):
    for link in li.find_all('a', href=True):
        path = link['href']

    for entry in li.find_all("a", class_="dotted"):
        size = re.search('\((.*)\)', entry.text)
        size = size.group(1).split(' ')[0]
        size = int(size)

        issueNum = entry.text.split(' ')[1]
        issueNum = int(issueNum)





    for date in li.find_all("p", class_="date"):
        date = date.text.split('/')

        date = date[2].strip() + '-' + date[1].strip() + '-' + date[0].strip() + ' 10:00:00'



    issueDict = {
        'path' : path,
        'size' : size,
        'number' : issueNum,
        'date' :  date
    }
    issueArray.append(issueDict)

    print(issueArray)