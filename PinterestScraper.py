import requests
import time
import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from sheetsDB import web_db_col

#main function
def getContent(link):
  #Open browser
  browser = webdriver.Chrome()

  #Go to link
  browser.get(link)

  #Pause
  time.sleep(5)

  #Click login button
  login_button = browser.find_element_by_css_selector("div[data-test-id='loginButton'][class='Jea XiG gjz mQ8 zI7 iyn Hsu'")
  login_button.click()

  #Pause
  time.sleep(2)
  
  #Login email
  email_field = browser.find_element_by_id('email')
  email_field.clear()
  email_field.send_keys('robgrootjen1@gmail.com')

  #Pause
  time.sleep(2)
  
  #Password
  password_field = browser.find_element_by_id('password')
  password_field.clear()
  password_field.send_keys('Strategy123')

  #Pause
  time.sleep(2)

  #Click login
  next_button = browser.find_element_by_css_selector("div[data-test-id='registerFormSubmitButton']")
  next_button.click()
  
  #Pause
  time.sleep(30)

  #Scroll time
  scroll_pause = 5

  #Get scroll height
  last_height = browser.execute_script("return document.body.scrollHeight")

  #List pins
  pinLinks = []
  cleanLinks = []

  while True:
    #Get pins
    #Source
    html = browser.page_source

    #Soup activate
    soup = BeautifulSoup(html,'lxml')

    #Find pins
    pinSoup = soup.find_all("a",href=True)

    #Look for links in pinSoup
    for x in pinSoup:
      x = x['href']
      pinLinks.append(x)

    #Cleaner pin links
    for y in pinLinks:
      if ('/pin/') in y:
        cleanLinks.append(y)
        
    #Scroll down to bottom
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    #Wait to load page
    time.sleep(scroll_pause)


    #Calculate new scroll height and compare with last scroll height
    new_height = browser.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
      break
    last_height = new_height

  #Cleanlinks
  cleanLinks = list(dict.fromkeys(cleanLinks))
    
  linkCount = len(cleanLinks)
  print('We have to check ' + str(linkCount) + ' pins.')
  
  #Main link
  mainLink = 'https://www.pinterest.com'

  #Countdown before process
  print('Starting process in...')
  time.sleep(1)
  print(3)
  time.sleep(1)
  print(2)
  time.sleep(1)
  print(1)
  time.sleep(1)

  #Website list
  webSites = []
  countdown = linkCount
  #Start website extraction
  for x in cleanLinks:
    
    print('Checking pin ' + str(countdown) + ' out of ' + str(linkCount) + '.')
    newPinLink = mainLink + x
    
    #Go to new browser
    browser.get(newPinLink)

    #Source
    html = browser.page_source

    #Soup activate
    soup = BeautifulSoup(html,'lxml')
    
    #Find and extract website
    site = soup.find("a", {"class":"linkModuleActionButton"})
    if site != None:
      site2 = site.text
      if site2 not in web_db_col:
        webSites.append(site2)
    else:
      continue
    
    countdown -= 1

  #Driver close
  browser.close()

  #Removing duplicates
  webSites = list(dict.fromkeys(webSites))
      
  #Converting to csv
  with open('pinterest.csv','w',newline='') as f:
    writer = csv.writer(f)
    for row in webSites:
      writer.writerow([row])

  webLen = str(len(webSites))

  print('Done! Process has been completed. ' + webLen + ' websites found.')


getContent('https://www.pinterest.com/search/pins/?q=Madagascar%20Reis&rs=typed&term_meta[]=Madagascar%7Ctyped&term_meta[]=Reis%7Ctyped')
