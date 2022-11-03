
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import requests
import pandas as pd


number = ''
pswd = ""
word_input = input("please enter the product name: ")
PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)
# driver.get("https://www.flipkart.com/")
# print(driver.title)
driver.get("https://www.flipkart.com/account/login?ret=/")
# time.sleep(2)
search = driver.find_element(By.CLASS_NAME, "_2IX_2-.VJZDxU")
# driver.find_element(By.)
search.send_keys(number)
search = driver.find_element(By.CLASS_NAME, "_2IX_2-._3mctLh.VJZDxU")
search.send_keys(pswd)
search.send_keys(Keys.RETURN)

curr_url = driver.current_url
driver.get(curr_url)
search = driver.find_element(By.CLASS_NAME, "_3704LK")
search.send_keys(word_input)
search.send_keys(Keys.RETURN)
url_link = ''
new_phones =[]
new_price = []
desc_list = []
img_url =[]
HEADERS = ({'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
            AppleWebKit/537.36 (KHTML, like Gecko) \
            Chrome/90.0.4430.212 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})
try:
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "_1YokD2._2GoDe3"))
    )
    url_link = driver.current_url
except:
    driver.quit()

print(url_link)
source = requests.get(url_link).text

soup = BeautifulSoup(source, 'lxml')

def find_details(type, parameter):
    details = soup.find_all(type, class_= parameter)
    data = [d.text for d in details]
    return data


phone = find_details('div', "_4rR01T")
desc = find_details('ul', '_1xgFaf')
price = find_details('div', "_30jeq3 _1_WHN1")

img = soup.find_all('img', class_= '_396cs4 _3exPp9')
img_urls = [d['src'] for d in img]
print(phone)
print(desc)
print(img_urls)
# print(offer)


print(len(phone))
print(len(desc))
print(len(img_urls))
print(len(price))
driver.quit()

data = pd .DataFrame({'model':phone, 'price':price, 'Description': desc, 'Image':img_urls})
data.to_excel(word_input+".xlsx")