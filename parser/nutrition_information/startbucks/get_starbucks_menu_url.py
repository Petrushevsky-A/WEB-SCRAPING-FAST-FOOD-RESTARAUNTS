import time

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
url = 'https://www.starbucks.co.uk/menu/drinks'
driver.get(url=url)
time.sleep(8)
# проблемы с куками
# driver.find_element(By.XPATH, '//div[@class = "pdynamicbutton"]').click()


sidebar_links = driver.find_elements(By.XPATH, '//*[contains(@class, "menu-sidebar-link")]')
links_menu = [i.get_attribute("href") for i in sidebar_links]
print(links_menu)
# for sidebar_elements in sidebar_links:
#     try:
#         sidebar_elements.click()
#         time.sleep(1)
#         menu_group = driver.find_element(By.XPATH, '//div[@class="menu-group"]')
#         links = [i.get_attribute("href") for i in menu_group.find_elements(By.XPATH, '//*[contains(@data-element-id, "menu-item")]')]
#         print(links)
#         links_foods.append(links)
#         time.sleep(2)
#     except:
#         print(sidebar_elements.text())
#         continue
#
# links_menu = sum(links_foods, [])



driver.close()
driver.quit()

data = {
    "links": links_menu
}

pd.DataFrame(data).to_excel('starbucks_url_menu.xlsx')
