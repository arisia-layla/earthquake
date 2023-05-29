# 대한민국 기상청 셀레니움 크롤링
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import json
from pyvirtualdisplay import Display
import pymysql
from selenium.webdriver.common.alert import Alert
import time
import pymysql
import random

conn = pymysql.connect(host='localhost', user='root', password='none', charset='utf8', database='quake') 
cursor = conn.cursor() 

option = Options()
option.add_argument("disable-infobars")
option.add_argument("disable-extensions")
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1309.0 Safari/537.17"
option.add_argument('user-agent=' + user_agent)
option.add_argument('disable-gpu')
option.add_argument('incognito')
option.add_argument('headless')
s = Service(ChromeDriverManager().install())
browser = webdriver.Chrome(service=s, options=option)

sql = "INSERT INTO dev (eq_count, eq_date, eq_time, eq_level, eq_addr1, eq_addr2, eq_location) VALUES (NULL, %s, %s, %s, %s, %s, %s)" 
j = 1
while True:
    url = f"https://www.weather.go.kr/w/eqk-vol/search/korea.do?startSize=1.0&endSize=999.0&pNo={j}&startLat=999.0&endLat=999.0&startLon=999.0&endLon=999.0&lat=999.0&lon=999.0&dist=999.0&keyword=&startTm=2018-12-11&endTm=2023-05-29&dpType=a"
    browser.get(url)
    loca = browser.find_element(By.CSS_SELECTOR, '#excel_body > tbody')
    for i in loca.find_elements(By.TAG_NAME, 'tr'):
        # cursor.execute(sql, ())
        date = i.find_element(By.CSS_SELECTOR, 'td:nth-child(2) > span').text
        date = str(date).split(" ")
        eq_date = date[0]
        eq_time = date[1]
        eq_level = str(i.find_element(By.CSS_SELECTOR, 'td:nth-child(3) > span').text)
        eq_addr1 = i.find_element(By.CSS_SELECTOR, 'td:nth-child(6) > span').text
        eq_addr2 = i.find_element(By.CSS_SELECTOR, 'td:nth-child(7) > span').text
        eq_location = i.find_element(By.CSS_SELECTOR, 'td:nth-child(8) > span').text
        print({"j":j, "date": eq_date, "time":eq_time, "level":eq_level, "addr1":eq_addr1, "addr2":eq_addr2, "location":eq_location})
        cursor.execute(sql, (eq_date, eq_time, eq_level, eq_addr1, eq_addr2, eq_location))
    conn.commit() 
    try:
        j += 1
    except:
        break
conn.close() 
    
# while True:
#     pass
