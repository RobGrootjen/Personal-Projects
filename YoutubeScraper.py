import requests
import time
import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from sheetsDB import youtube_db_col


#Main function
def getContent(link):
    #Open browser
    browser = webdriver.Chrome()

    #Go to link
    browser.get(link)

    #Pause
    time.sleep(15)

    #Youtube url
    youTube = 'https://www.youtube.com'

    #List
    urlList = []
    
    #Scroll down
    while True:
        #Get links
        #Source
        html = browser.page_source

        #Soup activate
        soup = BeautifulSoup(html,'lxml')

        #Find urls
        urlSoup = soup.find_all("a",href=True)

        #look for links in urlSoup
        for x in urlSoup:
          x = x['href']
          if len(x) > 0:
            if x[:3] == '/ch':
              if x not in youtube_db_col:
                urlList.append(x)

        #Pause
        time.sleep(1)

        #Scroll down
        browser.find_element_by_tag_name('body').send_keys(Keys.END)

        #No more results
        checkResult = soup.find("yt-formatted-string", {"id": "message","class": "style-scope ytd-message-renderer"})

        if checkResult != None:
          break

    #Driver close
    browser.close()
    
    #Remove duplicates
    urlList = list(dict.fromkeys(urlList))

    #Converting to csv
    with open('youtube.csv','w',newline='') as f:
        writer = csv.writer(f)
        for row in urlList:
          row = youTube + row
          writer.writerow([row])

    #Length list
    urlLen = str(len(urlList))

    #Process completed
    print('Done! Process has been completed. ' + urlLen + ' URL found.')

#URL
getContent('https://www.youtube.com/results?search_query=Australi%C3%AB+eTA')
