import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

pages = 2
driver = webdriver.Chrome(executable_path = 'tools/chromedriver')
driver.get("https://www.indeed.com.br/")
time.sleep(1)

what = driver.find_element_by_id('text-input-what')
what.send_keys('python')

where = driver.find_element_by_id('text-input-where')
where.send_keys('São Paulo')
where.submit()
time.sleep(1)

soup = BeautifulSoup(driver.page_source, 'lxml')
results = soup.findAll('a', {'class': 'jobtitle'})

jobs = driver.find_elements_by_class_name('jobtitle')
jobtitles = [job.get_attribute("innerHTML")[1:] for job in jobs]
print('===============================\n page 1')
print(jobtitles)

if pages > 1:
    jobtitles = []
    joblinks = []
    for i in range(1, pages+1):
        print('============================\n page', i)
        nextpage = driver.find_element_by_class_name('np')
        nextpage.click()
        time.sleep(2)
        try:
            print('Checking for pop up')
            close = driver.find_element_by_id('popover-close-link')
            close.click()
            print('Pop up closed')
        except:
            print('No pop up')

        jobs = driver.find_elements_by_class_name('jobtitle')
        for job in jobs:
            jobtitles.append(job.get_attribute("innerHTML")[1:])
            joblinks.append(job.get_attribute("href"))


d = {'job': jobtitles, 'link': joblinks}
df = pd.DataFrame(data=d)
print(df)

f = open('jobs.txt', 'a', encoding = 'utf-8')
for job in range(len(jobtitles)):
    title = jobtitles[job].replace('<b>','')
    title = title.replace('</b>','')
    link = joblinks[job]
    leng = 80 - len(title)
    space = ''
    for i in range(leng): space = space+'.'
    f.write(title+space+link+'\n')
f.close()