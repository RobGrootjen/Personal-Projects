import requests
import time
import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import re

#Main function
def getContent(link):
    #Open browser
    browser = webdriver.Chrome()

    #Go to google
    browser.get(link)

    #Pause
    time.sleep(5)

    #Search input
    searchQuery = 'ferreterias nicaragua'

    #Look for search bar and input
    search_Query = browser.find_element_by_name('q')
    search_Query.send_keys(searchQuery)

    #Pause
    time.sleep(1)

    #Click submit
    search_Query.submit()

    #Pause
    time.sleep(5)

    #List google url
    googleURL = []

    while True:
        #Get links
        html = browser.page_source

        #Soup activate
        soup = BeautifulSoup(html,'lxml')

        #Find urls
        urlSoup = soup.find_all('cite',attrs={'class':True})

        #Get urls one by one
        for x in urlSoup:
            x = x.get_text()
            x = x.split(" ")[0]
            googleURL.append(x)

        #Pause
        time.sleep(1)

        #Scroll down
        browser.find_element_by_tag_name('body').send_keys(Keys.END)

        #Pause
        time.sleep(1)

        #Find urls
        urlSoup = soup.find_all('cite',attrs={'class':True})

        #Find urls
        urlSoup = soup.find_all('cite',attrs={'class':True})

        #Get urls one by one
        for x in urlSoup:
            x = x.get_text()
            x = x.split(" ")[0]
            googleURL.append(x)

        #Pause
        time.sleep(1)

        #Check stop
        checkStop = soup.find(text='repetir la búsqueda e incluir los resultados omitidos')
        if checkStop != None:
            break

        #Go to next page
        next_page = browser.find_element_by_xpath("//span[contains(text(),'Siguiente')]")
        next_page.click()

    #Clean up list
    googleURL = list(dict.fromkeys(googleURL))

    #Length list
    urlLen = str(len(googleURL))

    #New clean List
    cleanList = []

    #Complete urls
    for x in googleURL:
        if 'www.' in x:
            x = 'https://' + x
            cleanList.append(x)
        else:
            x = 'https://www.' + x
            cleanList.append(x)

    #Process completed
    print(urlLen + ' URL found. Starting to scrape every URL.')

    #Length list
    urlLen = len(googleURL)

    #Main list
    gatherList = []

    #Activate for loop
    for x in cleanList:
        #Print URL # Check
        print('Checking URL ' + str(urlLen) + '.')

        #Lists
        nameList = []
        phoneList = []
        emailList = []
        urlList2 = []

        #Go to url
        try:
            browser.get(x)
        except:
            continue

        #Pause
        time.sleep(5)

        #Get getContent
        doc = browser.page_source

        #Soup activate
        sopaso = BeautifulSoup(doc,'lxml')

        #Find title and add title to list
        tremendaSopa = sopaso.title
        if tremendaSopa:
            tremendaSopa = tremendaSopa.get_text()
            nameList.append(tremendaSopa)
        else:
            nameList.append('NO TITLE')

        #Find phonenumber and add to list
        phones = re.findall(r'[\d]{4}-[\d]{4}', doc)
        if len(phones) >= 1:
            #Remove duplicate numbers
            phones = list(dict.fromkeys(phones))
            #Add to list
            phoneList.append(phones)
        else:
            phoneList.append('NO NUMBER')

        #Look for emails and add to list
        emails = re.findall(r'[\w\.-]+@[\w\.-]+.[\w\.-]', doc)
        if len(emails) >= 1:
            #Remove duplicate numbers
            emails = list(dict.fromkeys(emails))
            #Add to list
            emailList.append(emails)
        else:
            emailList.append('NO EMAIL')

        #Add url to List
        urlList2.append(x)

        #Gather List
        lolz = nameList + phoneList + emailList + urlList2
        gatherList.append(lolz)

        #-1
        urlLen -= 1

    #Converting list to csv
    with open ('prospects.csv','w',newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Empresa','Telefono','E-mail','Pagina Web'])
        for row in gatherList:
            writer.writerow([row])

    #Length List
    lenURL = str(len(gatherList))

    #Process completed
    print('Done! Process has been completed. ' + lenURL + ' prospects found.')

#URL
getContent('https://www.google.com/')
