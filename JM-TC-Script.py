# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 11:06:14 2019

@author: John
"""

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from datetime import date
import time
import csv

today = date.today()
today = today.strftime("%m%d%Y")

#Prepare the soup
site = "https://www.textcarrier.com/login.php"
chrome_options = Options()
#chrome_options.add_argument("--headless")
browser = webdriver.Chrome()#options=chrome_options)
browser.get(site)
time.sleep(1)
html = browser.page_source    
homepage = BeautifulSoup(html, 'lxml')

#Create CSV file (off_csv) and write headers
off_csv = "TextCarrier-{date}.csv".format(date=today)
off_headers = ["Number","First Name","Last Name","Subscribed To","Date Subscribed"]
off_file = open(off_csv, "w", newline='')
off_writer = csv.writer(off_file)
off_writer.writerow(off_headers)

#Login to service
def login():
    username = browser.find_element_by_name("email")
    username.clear()
    username.send_keys("USERNAME")
    
    password = browser.find_element_by_name("password")
    password.clear()
    password.send_keys("PASSWORD")

    browser.find_element_by_xpath("//input[@value='Login']").click()
    time.sleep(1)
    
def contact_scrape():
    contact_html = browser.page_source  
    contact_page = BeautifulSoup(contact_html, 'lxml')
    contact_table = contact_page.find("tbody")
    contact_rows = contact_table.find_all("tr")
    for contact in contact_rows:
       data = contact.get_text(separator=',')
       data_split = data.split(",")
       data_rough = [x for x in data_split if x != "\n"]
       if len(data_rough) < 11:
           data_rough.insert(1," ")
           data_rough.insert(2, " ")
       if len(data_rough) < 9:
           continue
       else:
           data_clean = data_rough[0:4]
           new_date = data_rough[4]+data_rough[5]
           data_clean.append(new_date)
           off_writer.writerow(data_clean)
       
if homepage.title.text == "Customer Login | TextCarrier.com":
    login()

browser.find_element_by_link_text("Subscribers").click()
time.sleep(1)

pages = 0
while pages < 500:
    try: 
        contact_scrape()
        browser.find_element_by_link_text("Next Page >>").click()      
        time.sleep(1)
        pages += 1
    except:
        break

off_file.close()

    
