import time
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

import pandas as pd

options = Options()
# options.add_argument("--headless")
# options.add_argument("--disable-extensions")
options.add_argument("--start-maximized")
options.add_argument("--lang=en-nz")
options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36")
options.add_argument("--disable-blink-features=AutomationControlled")



path = r'chromedriver.exe'
driver = webdriver.Chrome(chrome_options=options, executable_path=path)
driver.get(url='https://www.mcdonalds.com/gb/en-gb/menu.html')
time.sleep(3)
urls = [i.get_attribute("href") for i in driver.find_elements(By.XPATH, '//a[@class="category-link"]')]

links_foods = []
category = []

for id, url in enumerate(urls):
    driver.get(url=url)
    time.sleep(3)
    links = [i.get_attribute("href") for i in driver.find_elements(By.XPATH, '//a[@class="categories-item-link"]')]
    category_temp = driver.find_element(By.XPATH, '//h1[@id="category-item-title"]').text
    category.append([category_temp for i in links])
    time.sleep(3)
    print(links)
    print(category_temp)
    links_foods.append(links)


links_foods = sum(links_foods, [])
category = sum(category, [])


driver.close()
driver.quit()

data = {
    "links": links_foods,
    "category": category,
}
date = datetime.now().strftime("%d.%m.%Y")
pd.DataFrame(data).to_excel(f'mcdonalds_url_foods_{str(date)}.xlsx')