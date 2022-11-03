
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import requests
import pandas as pd

word_input = input("please enter the product name: ")
PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)
driver.get("https://www.amazon.in/")
print(driver.title)
search = driver.find_element(By.NAME, "field-keywords")

search.send_keys(word_input)
search.send_keys(Keys.RETURN)

url_link = ''
new_phones =[]
new_price = []
desc_list = []

try:
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "a-section.a-spacing-small.a-spacing-top-small"))
    )
    url_link = driver.current_url
except:
    driver.quit()

driver.quit()
HEADERS = ({'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
            AppleWebKit/537.36 (KHTML, like Gecko) \
            Chrome/90.0.4430.212 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})

# url_link = 'https://www.amazon.in/s?k=oppo&crid=1LIQOE7L83RJK&sprefix=oppo%2Caps%2C592&ref=nb_sb_noss_1'
print(url_link)
source = requests.get(url_link, headers=HEADERS).text
soup = BeautifulSoup(source, 'lxml')

# data = soup.find_all('div', class_="a-section a-spacing-small a-spacing-top-small")
phone =soup.find_all('a', class_ = "a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal")
new_phones = [d.text for d in phone]
print(len(new_phones))


price = soup.find_all('div', class_="a-row a-size-base a-color-base")

new_price = [d.text for d in price]
new_price = [d.split('₹')[1] for d in new_price]
print(new_price)

phone_count = len(new_phones)
price_count = len(new_price)
if price_count > phone_count:
    diff = price_count - phone_count
    for i in range(0, diff):
       del new_price[-1]

elif phone_count > price_count:
    diff1 = phone_count - price_count
    for i in range(0, diff1):
       del new_phones[-1]

print(len(new_phones),len(new_price))
# desc_list = [d.text for d in desc]
# print(desc_list)

data = pd .DataFrame({'model':new_phones, 'price':new_price})
print(data)
data.to_excel("new_oppo_models_amazon.xlsx")