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

urls = [
        'https://www.pret.co.uk/en-GB/products/categories/hot-drinks',
        'https://www.pret.co.uk/en-GB/products/categories/cold-drinks',
        'https://www.pret.co.uk/en-GB/products/categories/breakfast',
        'https://www.pret.co.uk/en-GB/products/categories/sandwiches-baguettes-and-wraps',
        'https://www.pret.co.uk/en-GB/products/categories/hot-food',
        'https://www.pret.co.uk/en-GB/products/categories/salads-and-protein-pots',
        'https://www.pret.co.uk/en-GB/products/categories/sweet-and-savoury-snacks',
        'https://www.pret.co.uk/en-GB/products/categories/fruit-and-fruit-pots',
        'https://www.pret.co.uk/en-GB/products/categories/pret-at-home',
        ]

links_foods = []
category = []
for url in urls:
    try:
        driver.get(url=url)
        time.sleep(3)
        links = [i.get_attribute("href") for i in driver.find_elements(By.XPATH, '//a[@data-testid="product-link"]')]
        category_temp = driver.find_element(By.XPATH, '//h1[@id="page-title"]').text
        category.append([category_temp for i in links])
        time.sleep(3)
        print(links)
        print(category)
        links_foods.append(links)
    except:
        continue

links_foods = sum(links_foods, [])
category = sum(category, [])


driver.close()
driver.quit()

data = {
    "links": links_foods,
    "category": category,
}
date = datetime.now().strftime("%d.%m.%Y")
pd.DataFrame(data).to_excel(f'pret_url_foods_{str(date)}.xlsx')
