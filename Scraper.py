from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
from urllib.request import Request, urlopen, urlretrieve
import os
import ssl
import datetime

# thread = '1929094'
# board = 'aco'
# url = 'https://boards.4chan.org/aco/thread/1929094'

thread = ''
board = ''
url = ''
saveFolder = ''

txt_message = ''
txt_thread = ''

numberOfContainers = 0
filesDownloaded = 0

class Scraper():

    def __init__(self, input_url, input_saveFolder):
        saveFolder = input_saveFolder
        url = input_url
        url = url.replace("https://boards.4chan.org/", "")
        url = url.replace("https://www.boards.4chan.org/", "")
        url = url.replace("boards.4chan.org/", "")
        board = url[:url.find("/")]
        thread = url.replace(board + "/thread/", "")
        url = input_url
        # print(board)
        # print(thread)
        # print(url)
        # I have no idea what this does :0
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        gcontext = ssl._create_unverified_context()  # Only for gangstars
        uClient = urlopen(req, context=gcontext)
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
        #Replacing /.\
        title = title.replace('/',' ')
        title = title.replace('.', ' ')
        title = title.replace('\\', ' ')
        # Making Directory
        if len(title) == 0:
            title = "Untitled"
        directory = saveFolder + board + "/" + title.strip()

        fileClass = postContainers[0].div.findAll("div", {"class": "file"})
        postImage = fileClass[0].a["href"]
        postImage = postImage[2:]

        if not os.path.exists(directory):
            os.makedirs(directory)

        if postImage.find("4cdn") > -1:
            ogSaveDirectory = directory + postImage[11 + len(board):]
            urlretrieve("https://" + postImage, ogSaveDirectory)

            # print("Error download image (1)")
        #(1) : Image has bad download name


        # Printing the details of post                                                                  #
        # print("Title: \t \t" + title)
        # print("OP: \t \t" + poster)
        # print("Time: \t \t" + postTime)
        # print("Post: \t \t" + postNumber)
        # print("Text:\t \t" + textInfo)
        # print("----------------------")
        # Saving the details of apost

        log_filename = title.strip() + postNumber + ".csv"
        f = open(log_filename, "w")
        headers = "Author, Time, Number, Message\n"
        f.write(headers)

        postContainers.remove(postContainers[0])

        numberOfContainers = len(postContainers)

        counter = 1

        for post in postContainers:
            print("Downloading file " + str(counter) +"/" + str(numberOfContainers))
            counter += 1
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
            # print("Poster: \t" + posterName)                                                          #
            # print("Time: \t\t" + postTime)
            # print("Post \t\t" + postNumber)
            # print("Text: \t\t" + postText)

            headers = posterName + "," + postTime +  "," + postNumber +  "," + postText.replace(',', '') + "\n"
            f.write(headers)

            # Downloading Attached Image
            try:
                fileClass = postInfo[0].findAll("div", {"class": "file"})
                postImage = fileClass[0].a["href"]
                postImage = postImage[2:]
                saveDirectory = directory + postImage[11 + len(board):]

                if postImage.find("4cdn") > -1:

                    if not os.path.isfile(saveDirectory):
                        # print(saveDirectory)
                        urlretrieve("https://" + postImage, saveDirectory)
                    # else:
                        # print("File already exists, skipping")                                        #
                # else:
                    # print("Error download image (1)")                                                 #
                    # (1) : Image has bad download name
            except:
                fartbox = 1

            os.system('clear')

            # print("----------------------")
        f.close()



    def getFilesDownloaded(self):
        return filesDownloaded