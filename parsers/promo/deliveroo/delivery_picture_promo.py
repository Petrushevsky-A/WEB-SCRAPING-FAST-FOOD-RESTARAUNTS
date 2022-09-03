import time
import itertools
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from datetime import datetime
import pandas as pd
import numpy as np

options = Options()
# options.add_argument("--headless")
# options.add_argument("--disable-extensions")
options.add_argument("--start-maximized")
options.add_argument("--lang=en-nz")
options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36")
options.add_argument("--disable-blink-features=AutomationControlled")



path = r'chromedriver.exe'



post_codes = [
        'W1C 1LX',
        'CF10 1PN',
        'BT1 5AA',
        'G1 3SQ',
        'B2 4QA',
        'L1 8JQ',
        'LS1 1UR',
        'M2 5DB',
        ]

url = 'https://deliveroo.co.uk/'

    #  $x('//li[contains(@class, "HomeFeedGrid")][3]/div[contains(@class, "HomeFeed")]/div/div//ul/li[contains(@class, "Slide")]')

for post_code in post_codes:
    driver = webdriver.Chrome(chrome_options=options, executable_path=path)
    time.sleep(2)
    driver.get(url=url)
    time.sleep(5)
    driver.find_element(By.XPATH, '//button[@id="onetrust-accept-btn-handler"]').click()
    time.sleep(1)

    # set input
    driver.find_element(By.XPATH, '//input[@id="location-search"]').send_keys(f'{post_code}')
    time.sleep(1)
    driver.find_element(By.XPATH, '//input[@id="location-search"]').send_keys(Keys.ENTER)
    time.sleep(8)
    try:
        driver.find_element(By.XPATH, '//button/span[text() = "OK"]').click()
        time.sleep(2)
    except:
        pass
    # нужно отлистать весь лист чтобы подгрузились все данные
    # нажимает еще пока не подгрузяться все таблички
    # '//h3[contains(text(),  "Up to")]/ancestor::li//ul[contains(@class, "Carousel")]'
    # для прогрузки информации необходимо прокрутить сайд бар
    data = []
    card_deals = driver.find_elements(By.XPATH, '//div[@id="home-feed-container"]/div/ul/li[2]//ul/li')
    print(len(card_deals))
    for id_card, card_deal in enumerate(card_deals, 1):
        def get_info_card(driver, id):
            try:
                link_images = driver.find_element(By.XPATH, f'//div[@id="home-feed-container"]/div/ul/li[2]//ul/li[{id}]//div[contains(@style, "background-image: url")]').get_attribute('style')[23:-3]
                info_card = "Not found"
            except:
                info_card = driver.find_element(By.XPATH,
                                                f'//div[@id="home-feed-container"]/div/ul/li[2]//ul/li[{id}]').text
                link_images = "Not found"


            date = datetime.now().strftime("%d.%m.%Y")
            city = driver.current_url.split('/')[4]
            return [date,post_code, city,  link_images, info_card]

        if card_deal.is_displayed():
            data.append(get_info_card(driver, id_card))

        else:
            button = driver.find_element(By.XPATH,
                                         '//div[@id="home-feed-container"]/div/ul/li[2]//button[@aria-label="Next"]')
            if not button.is_displayed():
                break
            else:
                button.click()
            time.sleep(3)

            data.append(get_info_card(driver, id_card))

    columns = {
        0: 'dates',
        1: 'post_codes',
        2: 'city',
        3: 'link_images',
        4: 'info_card',
    }

    print(data)

    data = pd.DataFrame(data)

    data = data.rename(columns=columns)
    date = datetime.now().strftime("%d.%m.%Y")
    data.to_excel(f'deliveroo_picture_card_{post_code}_{date}.xlsx')
    driver.close()
    driver.quit()
