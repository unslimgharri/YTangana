import sys, getopt
import json
import requests
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options


urlseed=str(sys.argv[1])

def gettitle(urlseed):
    mainContent = requests.get(urlseed)
    soup = BeautifulSoup(mainContent.text,'lxml')
    title = soup.find("meta",  property="og:title")
    title = title.get("content")
    return title

def savefile(url2, title):
    stitle=formatstring(title)
    song = requests.get(str(url2[0]), allow_redirects=True)
    with open(stitle, 'wb') as r:
        r.write(song.content)

def formatstring(title):
    stitle = ''
    for char in title:
        if char.isalnum():
            stitle += char
    stitle = str(stitle+'.mp3')
    return stitle

def generatedownload(urlseed):
    d = DesiredCapabilities.CHROME
    d['goog:loggingPrefs'] = {'performance':'ALL'}
    driver = webdriver.Chrome(desired_capabilities=d, service_args=["--verbose"])
    driver.get(urlseed)
    savelogs = driver.get_log('performance')
    line = str(json.dumps(savelogs, indent=4)).split('\\')
    link = [i for i in line if "mime=audio" in i]
    url2 = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', str(link))
    url2 = str(url2[0])
    url2 = url2.rsplit("&cver")
    return url2

downloadlink = generatedownload(urlseed)
title = gettitle(urlseed)
savefile(downloadlink, title)
