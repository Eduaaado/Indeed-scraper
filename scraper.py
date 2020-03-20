import time
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
import requests
from bs4 import BeautifulSoup
import pandas as pd

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
print(jobtitles)