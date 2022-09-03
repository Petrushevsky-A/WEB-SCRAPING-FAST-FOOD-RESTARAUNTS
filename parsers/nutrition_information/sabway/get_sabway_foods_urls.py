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
        'https://www.subway.com/en-GB/MenuNutrition/Menu/Signature-Wraps',
        'https://www.subway.com/en-GB/MenuNutrition/Menu/Salads',
        'https://www.subway.com/en-GB/MenuNutrition/Menu/The-Real-Deal-Sides',
        'https://www.subway.com/en-GB/MenuNutrition/Menu/Breakfast',
        'https://www.subway.com/en-GB/MenuNutrition/Menu/Kids',
        'https://www.subway.com/en-GB/MenuNutrition/Menu/SidesDrinksExtras',
        'https://www.subway.com/en-GB/MenuNutrition/Menu/Sandwiches',
        ]

links_foods = []
for url in urls:
    try:
        driver.get(url=url)
        time.sleep(3)
        links = [i.get_attribute("href") for i in driver.find_elements(By.XPATH, '//a[@class="menu-item-title"]')]
        time.sleep(3)
        print(links)
        links_foods.append(links)
    except:
        continue

links_foods = sum(links_foods, [])



driver.close()
driver.quit()

data = {
    "links": links_foods
}
date = datetime.now().strftime("%d.%m.%Y")
pd.DataFrame(data).to_excel(f'subway_url_foods_{str(date)}.xlsx')
