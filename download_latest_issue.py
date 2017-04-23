__author__ = 'mattmilliken'

from urllib.request import urlopen
from bs4 import BeautifulSoup
from download_past_issues import download_file
import os
import time
import sqlite3


LWB_URL = "https://lwb.co.nz/"
directorypath = 'LWB Issues/'


#Get the LWB main page, locate the "Latest Issue" section
r = urlopen(LWB_URL)
soup = BeautifulSoup(r, "html.parser")
soup.prettify()

current_issue =  (soup.find_all("div", class_="DownloadBox"))


for link in current_issue[0].find_all("a", href=True):

    current_issue_link = link['href']


#Download the file, get some descriptive info

issue_name = current_issue_link.split('/')[2]
issue_number = "".join(_ for _ in current_issue_link if _ in ".1234567890")

download_file(LWB_URL+current_issue_link, issue_name)
issue_size = round(os.path.getsize(directorypath+issue_name) / 1024 / 1024, 1)


#Connect to the database and store the info
conn = sqlite3.connect('lwb.db')

c = conn.cursor()

c.execute(

      "INSERT OR IGNORE INTO issues VALUES("+issue_number+"," +"'"+(current_issue_link)+"'"+","+str(issue_size)+","+"'" +time.strftime("%d-%m-%Y")+"')")

conn.commit()





