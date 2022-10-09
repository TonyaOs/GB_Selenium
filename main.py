import time
import json
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# для версии Chrome .103
service = Service('./chromedriver.exe')

driver = webdriver.Chrome(service=service)
driver.get('https://scrapingclub.com/exercise/basic_login')

WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID, 'id_name')))

login = driver.find_element(by=By.XPATH, value="//input[@id='id_name']")
password = driver.find_element(by=By.ID, value="id_password")

login.send_keys('scrapingclub')
password.send_keys('scrapingclub')

button_log = driver.find_element(by=By.XPATH, value="//button[@type='submit']").click()
WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'card-body')))

url = driver.find_element(by=By.XPATH, value="//a[contains(text(),'Scraping Infinite Scrolling Pages (Ajax)')]").get_attribute('href')

link_scroll = driver.find_element(by=By.XPATH, value="//a[contains(text(),'Scraping Infinite Scrolling Pages (Ajax)')]").click()
WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, 'card-body')))

first_height = driver.execute_script("return document.body.scrollHeight")
print(first_height)

while True:
    pause = random.randint(1,3)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    time.sleep(pause)

    next_height = driver.execute_script("return document.body.scrollHeight")
    print(next_height)
    if next_height == first_height:
        break
    first_height = next_height


clothes = driver.find_elements(by=By.XPATH, value="//div[@class='card']")
clothes_lst = []
for clo in clothes:
    image = clo.find_element(by=By.XPATH, value=".//img").get_attribute('src')
    link = clo.find_element(by=By.XPATH, value=".//a").get_attribute('href')
    name = clo.find_element(by=By.XPATH, value=".//h4[@class='card-title']").text
    price = clo.find_element(by=By.XPATH, value=".//h5").text
    print(image, link, name, price)
    info_dict = {
        'image': image,
        'link': link,
        'name': name,
        'price': price
    }
    clothes_lst.append(info_dict)

driver.quit()

with open('scroll_clothes.json', 'w', encoding='utf-8') as f:
    json.dump(clothes_lst, f)

