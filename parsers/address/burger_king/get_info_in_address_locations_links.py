import time
from datetime import datetime, timedelta

import requests

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
options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.53 Safari/537.36")
options.add_argument("--disable-blink-features=AutomationControlled")



path = r'chromedriver.exe'
driver = webdriver.Chrome(chrome_options=options, executable_path=path)


def get_head(driver):
    try:
        return driver.find_element(By.XPATH, '//*[contains(@class, "subtitle ")]').text
    except:
        return 'Not found'

def get_link_google_place(driver):
    try:
        return driver.find_element(By.XPATH, '//a[contains(@data-ya-track, "directions")]').get_attribute('href')
    except:
        return 'Not found'


def get_city(driver):
    try:
        return driver.find_element(By.XPATH, '//*[contains(@class, "city")]').text
    except:
        return 'Not found'

def get_region(driver):
    try:
        return driver.find_element(By.XPATH, '//*[contains(@class, "region")]').text
    except:
        return 'Not found'

def get_post_code(driver):
    try:
        return driver.find_element(By.XPATH, '//*[contains(@class, "postalCode")]').text
    except:
        return 'Not found'

def get_service(driver) -> dict[str: list]:
    try:
        service = driver.find_element(By.XPATH, '//ul[contains(@class, "Core-list")]').text
        service = {
            # из-за особенностей сохранения файла пришлось кинуть говнокода
            'Takeaway':'True' if 'Takeaway' in service else 'False',
            'Dine - in':'True' if 'Dine - in' in service else 'False',
            'Delivery':'True' if 'Delivery' in service else 'False',
            'No - contact delivery':'True' if 'No - contact delivery' in service else 'False',
            'Drive - through':'True' if 'Drive - through' in service else 'False',
        }

        return service
    except:
        return 'Not found'

def get_timework(driver) -> dict[str: list]:
    # '//table[contains(@class, "hours")]//tbody//tr/td[contains(text(), "Monday")]/following-sibling::td'
    def get_time(driver, day) -> str:
        try:
            return driver.find_element(By.XPATH, f'(//table[contains(@class, "hours")])[1]//tbody//tr/td[contains(text(), "{ day }")]/following-sibling::td').text
        except:
            return 'Not found - Not found'


    def split_time(time_work) -> tuple[datetime, datetime]:
        try:
            if time_work == 'Closed':
                return ('Closed', 'Closed')
            time = time_work.split(' - ')
            try:
                time_am = datetime.strptime(time[0], "%I:%M %p")
            except:
                time_am = 'Not found'
            try:
                time_pm = datetime.strptime(time[1], "%I:%M %p")
            except:
                time_pm = 'Not found'
            return (time_am, time_pm)
        except:
            return ('Not found', 'Not found')


    def get_delta_time(time_am: datetime, time_pm: datetime) -> str:
        try:
            if 'Closed' in (time_am, time_pm):
                return 'Closed'
            delta_time = time_pm - time_am
            return delta_time
        except:
            return 'Not found'

    def datetime_to_str(time) -> str:
        try:
            if time == 'Closed':
                return 'Closed'
            if isinstance(time, timedelta):
                return str(time)[:-3]
            return time.strftime('%H:%M')
        except Exception as ex:
            print(ex)
            return 'Not found'

    def get_tuple_time(time_work) -> tuple[str, str, str]:
        time_am, time_pm = split_time(time_work)
        delta_time = get_delta_time(time_am, time_pm)

        time_am, time_pm, delta_time = map(datetime_to_str, (time_am, time_pm, delta_time))

        return (time_am, time_pm, delta_time)

    days = (
        'Thursday',
        'Friday',
        'Saturday',
        'Sunday',
        'Monday',
        'Tuesday',
        'Wednesday',
    )

    # создаем словарь дней недели
    timework = {
        day: get_tuple_time(get_time(driver, day)) for day in days
    }




    # на выход структура {'day': [time_am, time_pm, time_delta]}
    # для исключений {'day': [time_am, 'Not found', 'Not found']}
    print(timework)
    return timework





def run_url(url, driver=driver):
    try:
        driver.get(url=url)
        time.sleep(2)
    except:
        pass



def get_links_restaurant():

    date = datetime.now().strftime("%d.%m.%Y")
    urls = pd.read_excel(f"bk_adress_restaurants_{str(date)}.xlsx")["urls"]
    data = []
    for url in urls:
        try:
            print(url)
            driver.get(url=url)
            time.sleep(3)
            head = get_head(driver)
            print(head)
            link_google = get_link_google_place(driver)
            print(link_google)
            city = get_city(driver)
            print(city)
            region = get_region(driver)
            print(region)
            post_code = get_post_code(driver)
            print(post_code)
            service = get_service(driver)
            print(service)
            timework = get_timework(driver)

            data.append(pd.Series({
                'head': head,
                'link_google': link_google,
                'city': city,
                'region': region,
                'post_code': post_code,
                'address': f'{city}, {region}, {post_code}',
                'Takeaway': service['Takeaway'],
                'Dine - in': service['Dine - in'],
                'Delivery': service['Delivery'],
                'No - contact delivery': service['No - contact delivery'],
                'Drive - through': service['Drive - through'],
                'Monday open': timework['Monday'][0],
                'Thursday open': timework['Thursday'][0],
                'Wednesday open': timework['Wednesday'][0],
                'Tuesday open': timework['Tuesday'][0],
                'Friday open': timework['Friday'][0],
                'Saturday open': timework['Saturday'][0],
                'Sunday open':timework['Sunday'][0],
                'Monday closing': timework['Monday'][1],
                'Thursday closing': timework['Thursday'][1],
                'Wednesday closing': timework['Wednesday'][1],
                'Tuesday closing': timework['Tuesday'][1],
                'Friday closing': timework['Friday'][1],
                'Saturday closing': timework['Saturday'][1],
                'Sunday closing': timework['Sunday'][1],
                'Monday delta': timework['Monday'][2],
                'Thursday delta': timework['Thursday'][2],
                'Wednesday delta': timework['Wednesday'][2],
                'Tuesday delta': timework['Tuesday'][2],
                'Friday delta': timework['Friday'][2],
                'Saturday delta': timework['Saturday'][2],
                'Sunday delta': timework['Sunday'][2],
                'url': url
            }))
        except:
            data.append(pd.Series({
                'head': 'Not found',
                'link_google': 'Not found',
                'city': 'Not found',
                'region': 'Not found',
                'post_code': 'Not found',
                'address': 'Not found',
                'Takeaway': 'Not found',
                'Dine - in': 'Not found',
                'Delivery': 'Not found',
                'No - contact delivery': 'Not found',
                'Drive - through': 'Not found',
                'Monday open': 'Not found',
                'Thursday open': 'Not found',
                'Wednesday open': 'Not found',
                'Tuesday open': 'Not found',
                'Friday open': 'Not found',
                'Saturday open': 'Not found',
                'Sunday open': 'Not found',
                'Monday closing': 'Not found',
                'Thursday closing': 'Not found',
                'Wednesday closing': 'Not found',
                'Tuesday closing': 'Not found',
                'Friday closing': 'Not found',
                'Saturday closing': 'Not found',
                'Sunday closing': 'Not found',
                'Monday delta': 'Not found',
                'Thursday delta': 'Not found',
                'Wednesday delta': 'Not found',
                'Tuesday delta': 'Not found',
                'Friday delta': 'Not found',
                'Saturday delta': 'Not found',
                'Sunday delta': 'Not found',
                'url': url,
            }))
            continue

    else:

        driver.close()
        driver.quit()

    pd.concat(data, axis=1).transpose().to_excel(f'burger_king_address_{date}.xlsx')
if __name__ == '__main__':
    get_links_restaurant()

