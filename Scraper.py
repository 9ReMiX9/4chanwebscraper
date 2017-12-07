from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
from urllib.request import Request, urlopen, urlretrieve
import os

thread = '11744904'
board = 'gif'
url = 'http://boards.4chan.org/gif/thread/11744904'

req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
uClient = urlopen(req)
page_html = uClient.read()
uClient.close()

page_soup = soup(page_html, "html.parser")

# Creates Array of postContainers
postContainers = page_soup.findAll("div", {"class": "postContainer"})
# Getting OP
opInfo = postContainers[0].div.findAll("div", {"class": "postInfo"})
# Finding Title Post
titleInfo = opInfo[0].findAll("span", {"class": "subject"})
title = titleInfo[0].text
# Finding OP
nameInfo = opInfo[0].findAll("span", {"class": "name"})
poster = nameInfo[0].text
# Finding Post Time
timeInfo = opInfo[0].findAll("span", {"class": "dateTime"})
postTime = timeInfo[0].text
# Finding Post Number
numberInfo = opInfo[0].findAll("span", {"class": "postNum"})
postNumber = numberInfo[0].text
# Finding Text
textInfo = postContainers[0].div.blockquote.text
#Replacing /
title = title.replace('/','-')
# Making Directory
directory = "H:/Documents/4ChanFolders/" + board + "/" + title.strip()

fileClass = postContainers[0].div.findAll("div", {"class": "file"})
postImage = fileClass[0].a["href"]
postImage = postImage[2:]

if not os.path.exists(directory):
    os.makedirs(directory)

ogSaveDirectory = directory + postImage[11 + len(board):]
urlretrieve("https://" + postImage, ogSaveDirectory)

print("Title: \t \t" + title)
print("OP: \t \t" + poster)
print("Time: \t \t" + postTime)
print("Post: \t \t" + postNumber)
print("Text:\t \t" + textInfo)
print("----------------------")

postContainers.remove(postContainers[0])

for post in postContainers:
    postInfo = post.findAll("div", {"class": "post reply"})
    # Finds Posters Name
    PostInfo = postInfo[0].findAll("div", {"class": "postInfo"})
    posterName = PostInfo[0].span.text
    # Finding Post Time & Number
    postTimeInfo = post.findAll("span", {"class": "dateTime"})
    postTime = postTimeInfo[0].text
    if "No." in postTime:
        postNumber = postTime[postTime.find("No."):]
        postTime = postTime[:postTime.find("No.")]
    else:
        postNumber = "Not Found"
        postTime = "Not Found"
    # Finds Text Attached
    postText = post.blockquote.text
    print("Poster: \t" + posterName)
    print("Time: \t\t" + postTime)
    print("Post \t\t" + postNumber)
    print("Text: \t\t" + postText)

    # Downloading Attached Image
    try:
        fileClass = postInfo[0].findAll("div", {"class": "file"})
        postImage = fileClass[0].a["href"]
        postImage = postImage[2:]
        saveDirectory = directory + postImage[11 + len(board):]
        print(saveDirectory)
        urlretrieve("https://" + postImage, saveDirectory)
    except:
        print("No Image")

    print("----------------------")
