import sys, getopt
import json
import requests
import re
import tkinter as tk
from tkinter.ttk import Progressbar
import time, threading
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
#from tqdm.utils import CallbackIOWrapper



def gettitle(urlseed):
    mainContent = requests.get(urlseed)
    soup = BeautifulSoup(mainContent.text,'lxml')
    title = soup.find("meta",  property="og:title")
    title = title.get("content")
    return title

def wgetfile(window, url2, title):
    stitle = formatstring(title)
    #window.text_box.insert(1.0,wget.download(str(url2[0]),stitle))

    r = requests.get(str(url2[0]), stream=True)
    filesize = int(r.headers.get('content-length', 0 ))
    block_size = 256
    cache=0
    #t = tqdm(total=filesize, unit='iB', unit_scale=True)
    window.progress_bar = Progressbar(mode='determinate', maximum=filesize)
    window.progress_bar.grid(row=3, column=0, sticky='we', padx=10, pady=10)
    def refresh(number):
        window.progress_bar.step(amount=number)
    with open(stitle, 'wb') as f:
        for data in r.iter_content(block_size):
            num=int(len(data))
            refresh(num)
            f.write(data)
    time.sleep(1)
    window.progress_bar.stop()
    window.text_box.insert(1.0,'Download finished song saved as: '+title+'\n')


def formatstring(title):
    stitle = ''
    for char in title:
        if char.isalnum():
            stitle += char
    stitle = str(stitle+'.mp3')
    return stitle


class Window():

    def __init__(self, root, **kwargs):
        self.window = root
        title = kwargs['name']
        self.window.title(title)
        #self.window.iconbitmap('logo1.ico')
        self.window.columnconfigure(0, pad=10)
        self.window.rowconfigure(0, pad=10)
        self.window.columnconfigure(1, pad=10)
        self.window.rowconfigure(1, pad=10)
        self.window.columnconfigure(2, pad=10)
        self.window.rowconfigure(2, pad=10)
        self.entry = tk.Entry()
        self.entry.grid(row=1, column=0, sticky='we', padx=5)
        self.text_box = tk.Text()
        self.text_box.grid(row=0, column=0)
        self.btn_download = tk.Button(text="Download", width=10, height=1, command=self.guiPrint)
        self.btn_download.grid(row=1, column=1, sticky='e', padx=5)

    def guiPrint(self):
        urlseed = self.entry.get()
        self.text_box.insert(1.0, 'Processing ' + urlseed + '\n')
        downloadlink = self.generatedownload(urlseed)
        title = gettitle(urlseed)
        download = threading.Thread(target=wgetfile, name='wgetfile', args=(self, downloadlink, title), daemon=True)
        download.start()

    def generatedownload(self, urlseed):
        d = DesiredCapabilities.CHROME
        d['goog:loggingPrefs'] = {'performance': 'ALL'}
        chrome_options = webdriver.ChromeOptions();
        chrome_options.add_experimental_option('excludeSwitches',
                                               ['load-extension', 'enable-automation', 'enable-logging'])
        driver = webdriver.Chrome(desired_capabilities=d, options=chrome_options)
        driver.get(urlseed)
        savelogs = driver.get_log('performance')
        line = str(json.dumps(savelogs, indent=4)).split('\\')
        link = [i for i in line if "mime=audio" in i]
        url2 = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', str(link))
        url2 = str(url2[0])
        url2 = url2.rsplit("&cver")
        return url2

def main():
    root = tk.Tk()
    window = Window(root=root, name='YTangana')
    root.mainloop()


if __name__ == '__main__':
    main()

#downloadlink = generatedownload(urlseed)
#title = gettitle(urlseed)
#savefile(downloadlink, title)
