#!/usr/bin/env python
# coding: utf-8

# In[142]:


get_ipython().system('pip install selenium')
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from random import randint
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv


# In[143]:


from selenium.webdriver.chrome.service import Service
s = Service('D:/Python/crawl data/chromedriver.exe')
browser = webdriver.Chrome()
#browser = webdriver.Chrome(service=s)


# In[144]:


browser.get("https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin")


# In[145]:


#load username, password
credential = open('data.txt')
line = credential.readlines()
userName = line[0]
password = line[1]


# In[146]:


#enter username
txtUser = browser.find_element(By.ID, "username")
txtUser.send_keys(userName)
time.sleep(randint(2,5))
print("**Finish fill username**")


# In[147]:


#enter password
txtPass = browser.find_element(By.ID, "password")
txtPass.send_keys(password)
time.sleep(randint(2,5))
print("**Finish fill password**")


# In[148]:


print("**Finish logging in**")


# In[149]:


search_query = str(input("What do you want to search?"))
search_field = browser.find_element(By.XPATH, '//*[@id="global-nav-typeahead"]/input')
search_field.send_keys(search_query)
search_field.send_keys(Keys.ENTER)
print('**Finish search ' + search_query + '**')
time.sleep(randint(2,5))


# In[150]:


#Click see all
button_see_all = browser.find_element(By.XPATH, '//*[@id="main"]/div/div/div[1]/div[2]/a')
button_see_all.click()


# In[151]:


#Scrape the URLs of the profiles
def Get_URL():
    page_source = BeautifulSoup(browser.page_source)
    profiles_link_button = page_source.find_all('div', class_ = 'entity-result__item')
    profiles_URLs = []
    for profile_link_button in profiles_link_button:
        #get URL
        profile = profile_link_button.find('a', class_ = 'app-aware-link')#Array
        profile_URL = profile.get('href')
        #Check access right if true is add URL to list profiles_URLs
        profile_true = profile_link_button.find('button', class_ = 'artdeco-button')
        if profile_true != None:
            if profile_URL not in profiles_URLs:
                profiles_URLs.append(profile_URL)
    return profiles_URLs


# In[152]:


#function return list URLs 
def Get_URLs_Pages():
    number_of_page = int(input('How many page do you want to search?'))
    URLs_all_page = []
    for page in range(number_of_page):
        URLs_one_page = Get_URL()
        #scroll the screen to the bottom page BY JavaScript
        browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
        time.sleep(randint(2,5))  
        #go to the next page
        #next_button = WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, 'artdeco-pagination__button--next')))
        next_button = browser.find_element(By.CLASS_NAME, 'artdeco-pagination__button--next')
        browser.execute_script("arguments[0].click();", next_button)# click by JavaScript
        time.sleep(randint(2,5))
        #Collet all URL of user to URLs_all_page
        URLs_all_page = URLs_all_page + URLs_one_page
    return URLs_all_page


# In[153]:


# page_source = BeautifulSoup(browser.page_source)
# profiles = page_source.find_all('div', class_ = 'entity-result')
# profiles
# # a = []
# # for profile in profiles:
# #     a.append(profile.find('button', class_ = 'artdeco-button'))
# # print(a)


# In[154]:


with open('D:/Python/crawl data/output.csv', 'w', newline = '') as f:
    headers = ['Name', 'Job', 'Location', 'URL']
    writer = csv.DictWriter(f, delimiter = ',', lineterminator = '\n', fieldnames = headers)
    writer.writeheader()
    #print NAME, JOB, LOCATION 
    URLs_all_page = Get_URLs_Pages()
    for link_URL in URLs_all_page:
        browser.get(link_URL)
        page_source = BeautifulSoup(browser.page_source, "html.parser")
        info_user = page_source.find('div', class_ = 'mt2 relative')
        tag_name = info_user.find('h1', class_ = 'text-heading-xlarge')
        name = tag_name.get_text().strip()
        print('Profile name is: ', name)
        tag_job = info_user.find('div', class_ = 'text-body-medium')
        job = tag_job.get_text().strip()
        print('Profile job is: ',job)
        tag_location = info_user.find('span', class_ = 'text-body-small')
        location = tag_location.get_text().strip()
        print('Profile location is: ',location)
        writer.writerow({headers[0]:name, headers[1]:job, headers[2]:location, headers[3]:link_URL})


# In[155]:


# browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
# #next_button = browser.find_element(By.CLASS_NAME, 'artdeco-pagination__button--next')
# next_button = WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, 'artdeco-pagination__button--next')))
# next_button.click()


# In[ ]:




