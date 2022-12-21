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
        'https://www.burgerking.co.uk/menu/section-abb64e87-84dd-43f1-89a8-d7094d5ae3b3',
        'https://www.burgerking.co.uk/menu/section-b896128c-9345-44fe-a3f6-72b32679005d',
        'https://www.burgerking.co.uk/menu/section-4a526bf3-ed0d-41f9-89af-ac84dd423c3e',
        'https://www.burgerking.co.uk/menu/section-67044bec-559c-4401-ac62-75f51a934698',
        'https://www.burgerking.co.uk/menu/section-4e51d826-c0f0-465e-83e9-db0e3c9b5c6f',
        'https://www.burgerking.co.uk/menu/section-a9b236a6-3898-4070-9c3b-d5396dd96590',
        'https://www.burgerking.co.uk/menu/section-4d66adf9-40b9-4c43-b575-56eab8c468e7',
        'https://www.burgerking.co.uk/menu/section-3668daf1-3feb-45fe-861d-25e0c4d63bef',
        'https://www.burgerking.co.uk/menu/section-878e95f0-1c8d-4085-86c8-aed04acc2664',
        ]

links_foods = []
category = []
category_temp = [
    'FRESH OFF THE GRILL',
    'FLAME-GRILLED BURGERS',
    'CRISPY & TENDER CHICKEN',
    'VEGGIE & PLANT BASED BURGERS',
    'SIDES',
    'KING SAVERS',
    'KING JR. MEALS',
    'DRINKS & COFFEE',
    'BREAKFAST',
]
for id, url in enumerate(urls):
    driver.get(url=url)
    time.sleep(3)
    links = [i.get_attribute("href") for i in driver.find_elements(By.XPATH, '//a[contains(@class, "tile-linkbk")]')]
    category.append([category_temp[id] for i in links])
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
pd.DataFrame(data).to_excel(f'burger_king_url_foods_{str(date)}.xlsx')