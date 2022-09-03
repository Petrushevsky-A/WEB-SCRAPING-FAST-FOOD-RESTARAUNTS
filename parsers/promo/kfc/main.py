

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

import pandas as pd
import numpy as np

options = Options()
# options.add_argument("--headless")
# options.add_argument("--disable-extensions")
options.add_argument("--start-maximized")
options.add_argument("--lang=en-nz")
options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36")
options.add_argument("--disable-blink-features=AutomationControlled")

import time

path = r'chromedriver.exe'
driver = webdriver.Chrome(chrome_options=options, executable_path=path)


urls = [
        'https://www.kfc.co.uk/menu/sharing',
        'https://www.kfc.co.uk/menu/for-one',
        'https://www.kfc.co.uk/menu/drinks',
        'https://www.kfc.co.uk/menu/snacks-extras',
        'https://www.kfc.co.uk/menu/treats',
        'https://www.kfc.co.uk/menu/vegan',
        'https://www.kfc.co.uk/menu/twisters-riceboxes-and-salads',
        ]

brand = 'kfc'
data = []
for url in urls:
    driver.get(url = url)
    time.sleep(5)
    category = driver.find_element(By.XPATH, '//h1').get_attribute('innerHTML')
    names = [i.get_attribute('innerHTML') for i in driver.find_elements(By.XPATH, '//div[@class="v4bgri-1 gHVvgF"]//h2')]
    descriptions = [i.get_attribute('innerHTML') for i in driver.find_elements(By.XPATH, '//div[@class="v4bgri-1 gHVvgF"]/a/div/p')]
    images = [i.get_attribute('src') for i in driver.find_elements(By.XPATH, '//div[@class="v4bgri-1 gHVvgF"]//img')]
    categorys = [category for i in names]
    for cat, name, description,image in zip(categorys, names,descriptions,images):
        data.append([brand, cat, name, description, image])
        print([brand, cat, name, description, image])

driver.close()
driver.quit()

data = np.array(data).T.tolist()

data ={
'brand':data[0],
'categorys':data[1],
'names':data[2],
'descriptions':data[3],
'images':data[4],
}



pd.DataFrame(data).to_excel('kfc_information.xlsx')