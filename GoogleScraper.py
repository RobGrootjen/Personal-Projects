import requests
import time
import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from sheetsDB import web_db_col

#Main function
def getContent(link):
    #Open browser
    browser = webdriver.Chrome()

    #Go to link
    browser.get(link)

    #Pause
    time.sleep(5)

    #Search input
    searchQuery = 'Nieuw-Zeeland Visum'

    #Look for search bar and input
    search_Query = browser.find_element_by_name('q')
    search_Query.send_keys(searchQuery)

    #Pause
    time.sleep(1)

    #Click submit
    search_Query.submit()

    #Pause
    time.sleep(5)
    
    #List google urls
    googleURL = []

    while True:
        #Get links
        #Source
        html = browser.page_source

        #Soup activate
        soup = BeautifulSoup(html,'lxml')

        #Find urls
        urlSoup = soup.find_all('cite',attrs={'class':True})
        

        #Get urls one by one
        for x in urlSoup:
          x = x.get_text()
          x = x.split(" ")[0]
          if x not in web_db_col:
            googleURL.append(x)

        #Pause
        time.sleep(1)

        #Scroll down
        browser.find_element_by_tag_name('body').send_keys(Keys.END)

        #Pause
        time.sleep(1)

        #Find urls
        urlSoup = soup.find_all('cite',attrs={'class':True})

        #Get urls one by one
        for x in urlSoup:
          x = x.get_text()
          x = x.split(" ")[0]
          if x not in web_db_col:
            googleURL.append(x)
              
        #Pause
        time.sleep(1)

        checkStop = soup.find(text='repetir la búsqueda e incluir los resultados omitidos')
        if checkStop != None:
            break
        
        #Go to next page
        next_page = browser.find_element_by_xpath("//span[contains(text(),'Siguiente')]")
        next_page.click()

    #Driver close
    browser.close()

    #Clean up list
    googleURL = list(dict.fromkeys(googleURL))

    #Converting to csv
    with open('google.csv','w',newline='') as f:
        writer = csv.writer(f)
        for row in googleURL:
            writer.writerow([row])

    #Length list
    urlLen = str(len(googleURL))

    #Process completed
    print('Done! Process has been completed. ' + urlLen + ' URL found.')
    
#URL
getContent('https://www.google.com/')
