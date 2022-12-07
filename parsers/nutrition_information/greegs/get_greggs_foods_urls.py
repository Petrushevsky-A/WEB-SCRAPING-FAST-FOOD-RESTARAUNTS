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
options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36")
# options.add_argument("--disable-blink-features=AutomationControlled")



path = r'chromedriver.exe'
driver = webdriver.Chrome(chrome_options=options, executable_path=path)
url = "https://www.greggs.co.uk/menu"
driver.get(url=url)
time.sleep(3)
driver.find_element(By.XPATH, '//button[contains(text(), "Accept")]').click()
time.sleep(1)

sidebar = driver.find_elements(By.XPATH, '//div[@id="scrollWrapper"]//button')


links_foods = []
category = []
for button_sidebar in sidebar[1:]:
    button_sidebar.click()
    time.sleep(2)
    links = [i.get_attribute("href") for i in driver.find_elements(By.XPATH, '//div[@class="max-w-screen-lg mx-auto"]//a')]
    category_temp = driver.find_element(By.XPATH, '//h2[contains(@class, "font-extrabold text-base")]').text
    category.append([category_temp for i in links])
    time.sleep(3)
    print(links)
    print(category)
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
pd.DataFrame(data).to_excel(f'greggs_url_foods_{str(date)}.xlsx')
