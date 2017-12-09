from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
from urllib.request import Request, urlopen, urlretrieve
import os
import datetime
import time
from Scraper import Scraper


board = "aco"
saveDirectory = "/root/" #SET THE SAVE POSITION
timesRun = 0

filesDownloadedTemp = 0
filesDownloadedTotal = 0

while 1 == 1:

    if timesRun % 2 != 0:
        board = 't'
    else:
        board = 'aco'

    timesRun += 1

    print(timesRun)

    for y in range(1,10):
        #Finding all pages from board
        if not y == 1:
            pageNumber = str(y)
        else:
            pageNumber = ''

        # print("Links for Page " + str(y) + ": ")

        req = Request("https://boards.4chan.org/" + board + "/" + pageNumber, headers={'User-Agent': 'Mozilla/5.0'})
        uClient = urlopen(req)
        page_html = uClient.read()
        uClient.close()
        page_soup = soup(page_html, "html.parser")
        threadContainers = page_soup.findAll("div", {"class": "thread"})

        for x in threadContainers:
            threadToDownload = Scraper("https://boards.4chan.org/aco/thread/" + x["id"][1:], saveDirectory)
            # print("Downloading thread https://boards.4chan.org/aco/thread/" + x["id"][1:])
            filesDownloadedTemp += threadToDownload.getFilesDownloaded()

    filesDownloadedTotal += filesDownloadedTemp
    print(str(filesDownloadedTemp) + " downloaded from last run")
    print(str(filesDownloadedTotal) + " downloaded in total")
    print("Ran " + timesRun + " times")
    time.sleep(300)

################################
# Things that need to get done
# Make a more visually pleasing output script
# Loop + Timer ability
# Multithreading