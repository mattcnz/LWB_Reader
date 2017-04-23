__author__ = 'mattmilliken'
import os
import sys
import re
from urllib.request import urlopen
from bs4 import BeautifulSoup

##Datebase Setup

import sqlite3
conn = sqlite3.connect('lwb.db')

c = conn.cursor()
c.execute('''
          CREATE TABLE IF NOT EXISTS issues
          (issueID INTEGER PRIMARY KEY ASC, path TEXT NOT NULL, size INTEGER, date TEXT)
          ''')

conn.commit()

#Create the Folder LWB Issues in whatever directory you run the script from

directory = "LWB Issues"

if not os.path.exists(directory):
    os.makedirs(directory)

directorypath = 'LWB Issues/'

#Downloads a file, writes to file_out
##EXAMPLE: download_file("https://media.readthedocs.org/pdf/pdfminer-docs/latest/pdfminer-docs.pdf", "test.pdf")
##Downlads that file and saves it as test.pdf

def download_file(file_url, file_out):
    response = urlopen(file_url)

    file = open(directorypath + file_out, 'wb')

    file.write(response.read())

    file.close()

    print("complete")



BASE_URL = "https://lwb.co.nz/issue-archive/?start="
START_URL_ID = 0
START_URL_INCREMENT = 20
START_URL_FINAL = 160

issueArray = []

if __name__ == "__main__":

    #Look through every issue on the LWB Website
    #Get the date, path, issue number and size of each issue, add these details to a dictionary
    #Save these dictionarys in issueArray
    #starts at https://lwb.co.nz/issue-archive/?start=0 and ends at start=160

    while START_URL_ID <= START_URL_FINAL:

        r = urlopen(BASE_URL + str(START_URL_ID))
        soup = BeautifulSoup(r, "html.parser")
        soup.prettify()


        issues = (soup.find_all("div", class_="mainContent ArchiveWidget"))

        for li in issues[0].find_all("li"):

            #Get's the path of the link ie. /assets/Uploads/ISSUE-596-WEB.pdf
            for link in li.find_all('a', href=True):
                path = link['href']

            #Gets the issue number and size of the pdf in MB
            for entry in li.find_all("a", class_="dotted"):
                size = re.search('\((.*)\)', entry.text)
                size = size.group(1).split(' ')[0]
                size = float(size)

                issueNum = entry.text.split(' ')[1]
                issueNum = int(issueNum)

            #Get's the date of the issue
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


        START_URL_ID += START_URL_INCREMENT


        #We now have a list of dictionarys called issueArray, where each entry represents an issue of the LWB
        #We can iterate over issueArray, and for each entry we can download it from the provided path and add it to the LWB Issues Directory

        ## CHANGE "for entry in issueArray:" to "for entry in issueArray[0:n]:" if you want to download n issues.
        

    for entry in issueArray:

        downloadPath = "https://lwb.co.nz/" + entry['path']
        download_file(downloadPath, str(entry['number'])+ '.pdf')

        c.execute(
              "INSERT OR IGNORE INTO issues VALUES("+str(entry['number'])+"," +"'"+(entry['path'])+"'"+","+str(entry['size'])+","+"'" +str(entry['date'])+"')")

        conn.commit()
