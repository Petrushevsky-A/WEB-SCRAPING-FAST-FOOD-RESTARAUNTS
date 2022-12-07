import time
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import pandas as pd
import numpy as np

options = Options()
# options.add_argument("--headless")
# options.add_argument("--disable-extensions")
options.add_argument("--start-maximized")
options.add_argument("--lang=en-nz")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.79 Safari/537.36")
options.add_argument("--disable-blink-features=AutomationControlled")



path = r'chromedriver.exe'



post_codes = [
        # 'W1C 1LX',
        # 'CF10 1PN',
        # 'BT1 5AA',
        # 'G1 3SQ',
        'B2 4QA',
        'L1 8JQ',
        'LS1 1UR',
        'M2 5DB',
        ]
# post_codes = [
#     "W2 1EB",
#     "W1W 7TN",
#     "WC1V 6PB",
#     "SW1V 1QT",
#     "W2 5QL",
#     "NW1 0JH",
#     "W9 2AD",
#     "NW5 2AE",
#     "CF24 0AB",
#     "CF10 5BZ",
#     "CF5 1GX",
#     "CF24 4NN",
#     "CF64 2AB",
#     "CF5 2BF",
#     "CF3 4AJ",
#     "CF14 4HE",
#     "BT9 6AA",
#     "BT15 2GZ",
#     "BT11 9AP",
#     "BT5 6QD",
#     "BT8 7HN",
#     "BT16 1YG",
#     "BT36 7QZ",
#     "BT28 1TP",
#     "G1 1LX",
#     "G12 8EL",
#     "G31 3AD",
#     "G42 9JT",
#     "G43 1TY",
#     "G51 4BH",
#     "G64 2AB",
#     "G33 3QE",
#     "B19 3JS",
#     "B16 8SU",
#     "B66 4PH",
#     "B29 6BD",
#     "B28 8AE",
#     "B23 6BA",
#     "B25 8UX",
#     "B68 0BS",
#     "L3 8JN",
#     "L5 5AA",
#     "CH41 6EY",
#     "L17 7BR",
#     "CH45 4JG",
#     "L18 2DA",
#     "L9 1GA",
#     "L12 9JH",
#     "LS2 8NJ",
#     "LS3 1JG",
#     "LS6 3NX",
#     "LS13 4LS",
#     "LS8 2AL",
#     "LS15 7NL",
#     "LS27 8QG",
#     "LS18 4DR",
#     "M3 1NN",
#     "M1 7HE",
#     "M4 7DB",
#     "M5 3AW",
#     "M14 6LE",
#     "M11 2SL",
#     "M21 9AN"
# ]


for post_code in post_codes[:]:
        print(post_code)
        url_brand = 'https://www.dominos.co.uk/mydominos/login'
        driver = webdriver.Chrome(chrome_options=options, executable_path=path)
        time.sleep(1)
        driver.get(url = url_brand)
        time.sleep(5)
        driver.find_element(By.XPATH, '//button[@id="onetrust-accept-btn-handler"]').click()

        # login
        login = 'projectlondon2022@protonmail.com'
        password = 'Projectplaner123!'
        driver.find_element(By.XPATH, '//div[@data-ref-id="login-email"]/input').send_keys(f'{login}')
        time.sleep(1)
        driver.find_element(By.XPATH, '//div[@data-ref-id="login-password"]/input').send_keys(f'{password}')
        time.sleep(1)
        driver.find_element(By.XPATH, '//button[@data-ref-id="login-btn"]').click()
        time.sleep(5)
        try:
                driver.find_element(By.XPATH, '//button[contains(@data-ref-id,"base-fulfilment-dialog__collect-button")]').click()
                time.sleep(2)
        except:
                pass



        date = datetime.now().strftime("%d.%m.%Y")
        # change
        links = driver.find_element(By.XPATH, '//a[contains(text(), "Deals")]')
        driver.execute_script("arguments[0].click();", links)
        time.sleep(3)
        driver.find_element(By.XPATH, '//div[@class="global-nav"]//li[1]/a').click()
        time.sleep(3)
        # driver.find_element(By.XPATH, '//div[@class="buttonContainer"]/button[contains(text(), "Change")]').click()
        driver.find_element(By.XPATH, '//*[contains(text(), "Change")]/ancestor::button').click()
        time.sleep(3)
        driver.find_element(By.XPATH, '//input').send_keys(f'{post_code}')
        time.sleep(1)

        driver.find_element(By.XPATH, '//input').send_keys(Keys.ENTER)
        time.sleep(2)
        try:
                driver.find_element(By.XPATH, '//*[contains(text(), "ll Collect")]').click()
                time.sleep(2)
        except:
                try:
                        driver.find_element(By.XPATH,
                                            '//div[@data-ng-show="handler.showLocalStore"]//button[contains(text(), "View Menu")]').click()
                        time.sleep(2)
                except:
                        driver.find_element(By.XPATH,
                                            '//div[@data-ng-show="handler.showLocalStore"]//button[contains(text(), "Deliver")]').click()
                        time.sleep(2)
        driver.find_element(By.XPATH, '//div[@class="global-nav"]//li[1]/a').click()
        time.sleep(3)

        # '//div[@class="store-address"]/div'
        address = [i.text for i in driver.find_elements(By.XPATH, '//span[contains(@data-ref-id, "address")]')[:-1]]
        print(address)
        post_code_address = address[-1]
        address = ", ".join(address)
        # Deals
        # driver.find_element(By.XPATH, '//div[@class="global-nav"]//li[3]/a').click()
        # driver.find_element(By.XPATH, '//div/*[contains(text(), "Deals")]').click()
        url = 'https://www.dominos.co.uk/deals/storedeals'
        driver.get(url=url)
        time.sleep(5)

        banners = [i.get_attribute('src') for i in driver.find_elements(By.XPATH, '//header[@class="banner banner-deals"]//img')]
        banner_list = []
        for id_banner, banner in enumerate(banners):
                banner_list.append([date, address, post_code, post_code_address, banner])
        print(banner_list)

        banner_list = pd.DataFrame(banner_list)

        columns = {
                0: 'dates',
                1: 'address',
                2: 'post_code',
                3: 'post_code_address',
                4: 'vouchers_name',
        }
        banner_list = banner_list.rename(columns=columns)
        date_for_save = datetime.now().strftime("%d.%m.%Y")
        banner_list.to_excel(f'dominos_banner_{post_code}_{str(date_for_save)}.xlsx')


        # '//span[contains(text(),  "VOUCHERS")]/ancestor::div[@class="deal-main-head"]/parent::div/div/article'
        vouchers = [i.text for i in driver.find_elements(By.XPATH, '//span[contains(text(),  "VOUCHERS")]/ancestor::div[@class="deal-main-head"]/parent::div/div/article//h5')]
        vouchers_list = []
        for id_voucher, voucher in enumerate(vouchers):
                vouchers_list.append([date, address, post_code, post_code_address, voucher])
        print(vouchers_list)

        vouchers_list = pd.DataFrame(vouchers_list)

        columns = {
                0: 'dates',
                1: 'address',
                2: 'post_code',
                3: 'post_code_address',
                4: 'vouchers_name',
        }
        vouchers_list = vouchers_list.rename(columns=columns)
        date_for_save = datetime.now().strftime("%d.%m.%Y")
        vouchers_list.to_excel(f'dominos_vouchers_{post_code}_{str(date_for_save)}.xlsx')

        collect_deals = []
        # '//section[@class="deal-category"]//article'
        for id_deal, deal in enumerate(driver.find_elements(By.XPATH, '//section[@class="deal-category"]//article'), 1):
                try:
                        collect_deals_name = driver.find_element(By.XPATH, f'//section[@class="deal-category"]//article[{id_deal}]//span[@class="deal-group-title h4"]').text
                except:
                        try:
                                collect_deals_name = driver.find_element(By.XPATH,
                                                                 f'//section[@class="deal-category"]//article[{id_deal}]//h5[@class="header-left deal-card-header"]').text
                        except:
                                collect_deals_name = "empty"
                try:
                        collect_deals_description = driver.find_element(By.XPATH, f'//section[@class="deal-category"]//article[{id_deal}]//p').text
                except:
                        collect_deals_description = ''

                try:
                        collect_deal_img = driver.find_element(By.XPATH,
                                                                f'//section[@class="deal-category"]//article[{id_deal}]//img').get_attribute('src')
                except:
                        try:
                                collect_deal_img = driver.find_element(By.XPATH,
                                                                f'//section[@class="deal-category"]//article[{id_deal}]//p').value_of_css_property('background-image')
                        except:
                                collect_deal_img = 'empty'
                try:
                        collect_deal_count_deals = driver.find_element(By.XPATH, f'//section[@class="deal-category"]//article[{id_deal}]//span[@class="deal-group-count h4"]').text
                except:
                        collect_deal_count_deals = ''
                collect_deals.append([date, address, post_code,post_code_address, collect_deals_name, collect_deals_description, collect_deal_img, collect_deal_count_deals])
                print(date, address, post_code,post_code_address, collect_deals_name, collect_deals_description, collect_deal_img, collect_deal_count_deals)


        columns = {
                0: 'dates',
                1: 'address',
                2: 'post_code',
                3: 'post_code_address',
                4: 'collect_deals_name',
                5: 'collect_deals_description',
                6: 'collect_deal_img',
                7: 'collect_deal_count_deals',

            }

        print(collect_deals)

        collect_deals = pd.DataFrame(collect_deals)

        collect_deals = collect_deals.rename(columns=columns)
        date = datetime.now().strftime("%d.%m.%Y")
        collect_deals.to_excel(f'dominos_collect_deals_{post_code}_{str(date)}.xlsx')

        driver.close()
        driver.quit()