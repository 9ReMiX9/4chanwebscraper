from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
from urllib.request import Request, urlopen, urlretrieve
import os
import datetime
from Scraper import Scraper


board = "aco"
saveDirectory = "/root/" #SET THE SAVE POSITION

for y in range(1,10):
    #Finding all pages from board
    if not y == 1:
        pageNumber = str(y)
    else:
        pageNumber = ''

    print("Links for Page " + str(y) + ": ")

    req = Request("https://boards.4chan.org/" + board + "/" + pageNumber, headers={'User-Agent': 'Mozilla/5.0'})
    uClient = urlopen(req)
    page_html = uClient.read()
    uClient.close()
    page_soup = soup(page_html, "html.parser")
    threadContainers = page_soup.findAll("div", {"class": "thread"})

    for x in threadContainers:
        threadToDownload = Scraper("https://boards.4chan.org/aco/thread/" + x["id"][1:], saveDirectory)
        print("Downloading thread https://boards.4chan.org/aco/thread/" + x["id"][1:])