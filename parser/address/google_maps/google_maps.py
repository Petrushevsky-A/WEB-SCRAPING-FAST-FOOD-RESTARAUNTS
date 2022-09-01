import time
from typing import Dict, Union, Any

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service


from multiprocessing import Pool
import numpy as np
import pandas as pd
from datetime import datetime
import re


class ParseGoogle():
    # Парсер принимает на вход URL ссылку торговой точки.
    # Выход пандас обьект в 1 строку для дальнейшей конкатенации - метод Get().

    def __init__(self, url):
        self.url = url
        self.about_pressed = False
        self.name_building = None
        self.address = None
        self.geo_lat_long = None
        self.time_work_days = None
        self.plus_code = None
        self.delivery_sites = None
        self.site = None
        self.phone = None
        self.contactless_delivery = None
        self.takeawey_food = None
        self.food_in_the_establishment = None
        self.delivery = None
        self.average_rating = None
        self.number_of_reviews = None
        self.time_open = None
        self.time_closing = None
        self.time_interval = None
        self.city = None
        self.post_code = None
        self.drive_through = None
        self.dine_in = None
        self.dine_in = None
        # не ну мало ли заглюк, гет вернет строку с None
        try:
            options = Options()
            # options.add_argument("--headless")
            # options.add_argument("--disable-extensions")
            options.add_argument("--lang=en-nz")
            options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36")
            path = r'chromedriver.exe'
            self.driver = webdriver.Chrome(chrome_options=options, executable_path=path)
            self.driver.get(url=self.url)
            self.run()
            self.driver.close()
            self.driver.quit()
        except Exception:
            self.driver.close()
            self.driver.quit()


    #Получение геоданных широты / долготы Вывод: широта / долгота
    def get_geo_lat_long(self):
        # запускать после гет плюса
        # из адреса путем регулярки
        # "https://plus.codes/map"
        # открываем окно
        # гуглим
        try:
            url = "https://plus.codes/map"
            self.driver.get(url=url)
            time.sleep(3)
            print(self.plus_code)
            self.driver.find_element(By.XPATH, '//input[@id = "search-input"]').send_keys(f"{self.plus_code}")
            time.sleep(2)
            self.driver.find_element(By.XPATH, '//input[@id = "search-input"]').send_keys(Keys.RETURN)
            time.sleep(2)
            self.driver.find_element(By.XPATH, '// *[ @ id = "summary"] / div[1]').click()
            time.sleep(2)
            lat_long = self.driver.find_element(By.XPATH, '//*[@id="placecard-details"]/div[3]/div[1]').text
            print(lat_long)
            return lat_long
        except Exception:
            return "NotFound"

    #
    # Убрать великобритания
    def get_address(self):
        try:
            time.sleep(1)
            return self.driver.find_element(By.XPATH, "//*[@data-item-id = 'address']").text
        except Exception:
            return "NotFound"
    #
    def get_name_building(self):
        try:
            return self.driver.find_element(By.XPATH, '//h1').text
        except Exception:
            return "NotFound"
    #
    def get_city(self):
        try:
            city = self.address.split(",")
            for i in city:
                if self.post_code in i:
                    return i.replace(self.post_code, "").strip()
        except Exception:
            return "NotFound"
    #
    def get_area(self):
        # из адреса путем регулярки
        pass

    #
    def get_post_code(self):
        try:

            # post_code = re.findall(r" .{1,5} .{1,5}, United Kingdom", self.address)[0].replace(", United Kingdom", "").strip()
            address = self.address.split(', ')[-1]
            post_code = " ".join(address.split()[1:])

            # [0].replace(", Великобритания", "").strip
            print(post_code)
            return post_code
        except Exception:
            return "NotFound"
    #Дополнительный код геоданных торговой точки, возможно будет необходима для иных источников парса. Вывод: Строка str
    def get_plus_code(self):
        try:
            time.sleep(1)
            return self.driver.find_element(By.XPATH, '//*[contains(@aria-label, "Plus")]').text
            # return self.driver.find_element(By.XPATH, "//*[@data-item-id = 'oloc']/div[1]/div[2]/div[1]").text
        except Exception:
            return "NotFound"
        #     //child::*
        # /div[1]/div[2]/div[1]

    #Получение брэнда торговой точки Вывод: Строка str
    def get_brand(self):
        # из сайта
        pass

    #Словарь времени работы по дням Вывод: Словарь Dict


    def get_time_work_days(self):
        try:
            print("Run get time type 2")
            self.driver.find_element(By.XPATH, '//*[@data-item-id="oh"]').click()
            time.sleep(1)
            days_time_work = {}

            # Потребовалась прямая передача self для взятия контроля над драйвером. Глобальная переменная self не работает внутри вложенных функций
            def get_day_name(num, self):
                try:
                    return self.driver.find_element(By.XPATH,
                                                    f"//*[contains(@aria-label, 'Friday')]/div/table/tbody/tr[{num}]/td[1]/div[1]").get_attribute(
                        'innerHTML').capitalize()
                except Exception:
                    return 'NotFound'

            def get_time_work_day(num, self):
                try:
                    return self.driver.find_element(By.XPATH,
                                                    f"//*[contains(@aria-label, 'Friday')]/div/table/tbody/tr[{num}]/td[2]/ul/li").get_attribute(
                        'innerHTML')
                except Exception:
                    return 'NotFound'

            print("===GET TIME WORK=====")
            print("=======Type 2========")
            for i in range(1, 8):
                name_day = get_day_name(i, self)
                time_work_day = get_time_work_day(i, self)
                days_time_work[name_day] = time_work_day
                print(f"{name_day} : {days_time_work[name_day]}")
            print("=====================")
            print(days_time_work)
            time.sleep(2)
            try:
                self.driver.find_element(By.XPATH, '//*[@id="pane"]/div/div[1]/div/div/div[1]/div/div/div[1]/span/button').click()
            except:
                self.driver.get(url=self.url)
                time.sleep(5)
            time.sleep(2)
            return days_time_work
        except Exception as ex:
            try:# Если стандартный раскрывающийся блок тайм

                days_time_work = {}
                # Потребовалась прямая передача self для взятия контроля над драйвером. Глобальная переменная self не работает внутри вложенных функций
                def get_day_name(num, self):
                    try:
                        return self.driver.find_element(By.XPATH, f"//*[contains(@aria-label, 'Friday')]/div/table/tbody/tr[{num}]/td[1]/div[1]").get_attribute('innerHTML').capitalize()
                    except Exception:
                        return 'NotFound'
                def get_time_work_day(num, self):
                    try:
                        return self.driver.find_element(By.XPATH, f"//*[contains(@aria-label, 'Friday')]/div/table/tbody/tr[{num}]/td[2]/ul/li").get_attribute('innerHTML')
                    except Exception:
                        return 'NotFound'

                print("===GET TIME WORK=====")
                print("=======Type 1========")
                for i in range(1, 8):
                    name_day = get_day_name(i, self)
                    time_work_day = get_time_work_day(i, self)
                    days_time_work[name_day] = time_work_day
                    print(f"{name_day} : {days_time_work[name_day]}")
                print("=====================")
                print(days_time_work)
                return days_time_work

            except:
                return { 'Tuesday': 'NotFound', 'Wednesday': 'NotFound', 'Thursday': 'NotFound',
                         'Friday': 'NotFound', 'Saturday': 'NotFound', 'Sunday': 'NotFound',
                         'Monday': 'NotFound',}


    #Cписок доменов сайтов всплывающих по кнопке "Оформит заказ" Вывод: список List
    def get_delivery_sites(self):
        try:
            # Возможно нужно исключение при "Закрыто", "Закрыто на совсем" или при отсутсвии. Возможны иные варианты
            self.driver.find_element(By.XPATH, '//*[@aria-label="Place an order"]').click()
            time.sleep(1)
            temp = []
            for i in range(1, 100):
                try:
                    temp.append(self.driver.find_element(By.XPATH,
                                f"//*[contains(@jsan, 'section-scrollbox')]/div[1]/div[{i}]/button/div[1]/div[2]/div[1]").text
                                )
                except:
                    break
            time.sleep(1)
            try:
                self.driver.find_element(By.XPATH, '//*[@aria-label="Close"]').click()
            except:
                self.driver.get(url=self.url)
                time.sleep(2)
            time.sleep(1)
            return temp
        except Exception:
            self.driver.get(url=self.url)
            time.sleep(3)
            return "NotFound"
    #Получение домена сайта торговой точки
    def get_site(self):
        try:
            time.sleep(1)
            return self.driver.find_element(By.XPATH, "//*[contains(@data-item-id, 'authority')]").text.strip()
        except Exception:
            return "NotFound"
    #Получение номера телефона
    def get_phone(self):
        try:
            time.sleep(1)
            return self.driver.find_element(By.XPATH, "//*[contains(@data-item-id, 'phone')]").text.strip()
        except Exception:
            return "NotFound"


    def get_delta_work_time(self):
        # {'Tuesday': '11AM–10PM', 'Wednesday': '11AM–10PM', 'Thursday': '11AM–10PM', 'Friday': '11AM–10PM',
        #  'Saturday': '11AM–10PM', 'Sunday': '11AM–10PM', 'Monday': '11AM–10PM'}

        # {'Tuesday': '7AM–5PM', 'Wednesday': '7AM–5PM', 'Thursday': '7AM–5PM', 'Friday': '7AM–5PM',
        #  'Saturday': '7:30AM–5PM', 'Sunday': '8AM–3PM', 'Monday': '7AM–5PM'}

        # {'Tuesday': '7AM–5PM', 'Wednesday': '7AM–5PM', 'Thursday': '7AM–5PM', 'Friday': '7AM–5PM',
        #  'Saturday': '8AM–4PM', 'Sunday': 'Closed', 'Monday': '7AM–5PM'}

        # {'Tuesday': '6AM–12AM', 'Wednesday': '6AM–12AM', 'Thursday': '6AM–12AM', 'Friday': '6AM–12AM',
        #  'Saturday': '6AM–12AM', 'Sunday': '6AM–12AM', 'Monday': '6AM–12AM'}

        # {'Tuesday': '10:30AM–1AM', 'Wednesday': '10:30AM–1AM', 'Thursday': '10:30AM–2AM', 'Friday': '10:30AM–2AM',
        #  'Saturday': '10:30AM–2AM', 'Sunday': '11AM–1AM', 'Monday': '10:30AM–1AM'}
        try:
            time_open = {}
            time_closing = {}
            time_interval = {}
            print("=====GET DELTA TIME=====")

            def normalize_time(time_work):
                time_work = time_work.upper()
                # print(time_work)
                try:
                    if time_work == 'CLOSED':
                        return ['Closed', 'Closed']
                    if time_work == 'OPEN 24 HOURS':
                        return ['1 00:00', '2 00:00']
                    time_1, time_2 = time_work.split('–')
                    time_1_meridiem = ''
                    # print(f'time_1 {time_1}')
                    # print(f'time_2 {time_2}')
                    # time  1 normalize
                    if 'AM' in time_1:
                        time_1 = time_1.replace('AM', '')
                        time_1_meridiem = 'AM'

                    if 'PM' in time_1:
                        time_1 = time_1.replace('PM', '')
                        if ':' in time_1:
                            time_1_hour, time_1_minutes = time_1.split(':')
                            time_1_hour = int(time_1_hour) + 12
                            time_1 = f'{time_1_hour}:{time_1_minutes}'
                        time_1_meridiem = 'PM'

                    if not ':' in time_1:
                        time_1 = f'{time_1}:00'
                    time_1_result = f'1 {time_1}'

                    # print(f'time_1_result {time_1_result}')

                    # time  2 normalize
                    time_2_meridiem = ''
                    time_2_day = 1
                    if 'AM' in time_2:
                        time_2 = time_2.replace('AM', '')
                        time_2_meridiem = 'AM'

                    if 'PM' in time_2:
                        time_2 = time_2.replace('PM', '')
                        if ':' in time_2:
                            time_2_hour, time_2_minutes = time_2.split(':')
                            time_2_hour = int(time_2_hour) + 12
                            time_2 = f'{time_2_hour}:{time_2_minutes}'
                        else:
                            time_2 = f'{int(time_2) + 12}'
                        time_2_meridiem = 'PM'

                    if not ':' in time_2:
                        time_2 = f'{time_2}:00'



                    AMAM = time_1_meridiem == 'AM' and time_2_meridiem == 'AM'
                    PMPM = time_1_meridiem == 'PM' and time_2_meridiem == 'PM'
                    PMAM = time_1_meridiem == 'PM' and time_2_meridiem == 'AM'

                    # print(AMAM,PMPM,PMAM)


                    meridiem = any([AMAM, PMPM, PMAM])
                    # print(meridiem)
                    # print(f'time_2 {time_2}')
                    time_compare = datetime.strptime(time_1, "%H:%M") > datetime.strptime(time_2, "%H:%M")
                    if meridiem and time_compare:
                        time_2_day = 2

                    time_2_result = f'{time_2_day} {time_2}'
                    # print(f'time_2_result {time_2_result}')
                #     print(f'{time_1} - {time_2}')
                #     print(f'{datetime.strptime(time_1, "%H:%M") > datetime.strptime(time_2, "%H:%M")}')
                except:
                    #         если накинули говна на вентилятор
                    time_1_result = "Not found"
                    time_2_result = "Not found"
                return [time_1_result, time_2_result]


            for i in self.time_work_days:
                time_open[i], time_closing[i] = normalize_time(self.time_work_days[i])

            # print(f'time_open {time_open}')
            # print(f'time_closing {time_closing}')
            def delta_time(time):
                time_1, time_2 = time
                if 'CLOSED' in time:
                    return 'Closed'
                if 'Not found' in time:
                    return 'Not found'
                if time_1 == '1 00:00' and time_2 == '2 00:00':
                    return '24:00'
                date_1 = datetime.strptime(time_1, "%d %H:%M")
                date_2 = datetime.strptime(time_2, "%d %H:%M")
                time_interval = str(date_2 - date_1)[:-3]
                return time_interval

            for i in self.time_work_days:
                time_interval[i] = delta_time([time_open[i], time_closing[i]])
            # print(f'time_interval {time_interval}')
            def time_to_number(time):
                try:
                    list_num = time.split(':')
                    result = int(list_num[0]) + int(list_num[1]) / 60
                    if len(str(result)) > 4:
                        return f"{result:.2f}"
                    elif list_num[1] == '00':
                        return f"{list_num[0]}"
                    else:
                        return f"{result}"
                except:
                    return time

            for i in self.time_work_days:
                time_interval[i] = time_to_number(f'{time_interval[i]}')

            for i in self.time_work_days:
                if 'Closed' in time_open[i]:
                    time_open[i] = 'Closed'
                    continue
                if 'Not found' in time_open[i]:
                    time_open[i] = 'Not found'
                    continue
                if 'Closed' in time_closing[i]:
                    time_closing[i] = 'Closed'
                    continue
                if 'Not found' in time_closing[i]:
                    time_closing[i] = 'Not found'
                    continue
                time_open[i] = str(time_open[i])[2:]
                time_closing[i] = str(time_closing[i])[2:]


            return time_open, time_closing, time_interval
        except:
            answer = {'Tuesday': 'NotFound', 'Wednesday': 'NotFound', 'Thursday': 'NotFound',
             'Friday': 'NotFound',
             'Saturday': 'NotFound', 'Sunday': 'NotFound', 'Monday': 'NotFound'}
            return answer, answer, answer

    # def time_to_number(self):
    #     answer = {}
    #     for i in self.time_interval:
    #         try:
    #             list_num = self.time_interval[i].split(':')
    #             result = int(list_num[0]) + int(list_num[1]) / 60
    #             if len(str(result)) > 4:
    #                 answer[i] = f"{result:.2f}"
    #             elif list_num[1] == '00':
    #                 answer[i] =  f"{list_num[0]}"
    #             else:
    #                 answer[i] = f"{result}"
    #         except:
    #             answer[i] = number
    #     return answer
    #Переключение на категории(обратно не переключает) возможна переделка в декоратор
    def click_about(self):
        try:
            if self.about_pressed == False:
                self.driver.find_element(By.XPATH, "//button[contains(@jsaction, 'pane.attributes.expand;ptrdown:ripple.play;mousedown:ripple.play;keydown:ripple.play')]").click()
                time.sleep(2)
                self.about_pressed = True
            return None
        except Exception:
            return "NotFound"
    # # Бесконтактная доставка
    # def is_contactless_delivery(self):
    #     self.click_about()
    #     return self.driver.find_element_by_xpath("//*[contains(@aria-label, 'Есть бесконтактная доставка')]").text
    #
    # # Еда навынос
    # def is_takeawey_food(self):
    #     self.click_about()
    #     return self.driver.find_element_by_xpath("//*[contains(@aria-label, 'Заказы на вынос')]").text
    #
    # # Еда в заведении
    # def is_food_in_the_establishment(self):
    #     self.click_about()
    #     return self.driver.find_element_by_xpath("//*[contains(@aria-label, 'Еда в заведении')]").text
    #
    # # Доставка
    # def is_delivery(self):
    #     self.click_about()
    #     return self.driver.find_element_by_xpath("//*[contains(@aria-label, 'Доставка')]").text

    # ===================================================

    # Предлагаемые варианты
    # Бесконтактная доставка
    def is_contactless_delivery(self):
        try:
            self.click_about()
            return self.driver.find_element(By.XPATH, "//*[contains(@aria-label, 'Has no-contact delivery')]").text
        except Exception:
            return "NotFound"
    # Еда навынос
    def is_takeawey_food(self):
        try:
            self.click_about()
            return bool(self.driver.find_element(By.XPATH, '//*[@aria-label="Offers takeaway"]').text)
        except Exception:
            return False

    # Еда в заведении
    def is_food_in_the_establishment(self):
        try:
            self.click_about()
            return self.driver.find_element(By.XPATH, "//*[contains(@aria-label, 'Еда в заведении')]").text
        except Exception:
            return "NotFound"
    # Доставка
    def is_delivery(self):
        try:
            self.click_about()
            return bool(self.driver.find_element(By.XPATH, "//*[contains(@aria-label, 'Offers delivery')]").text)
        except Exception:
            return False
    # ===================================================

    # Это должно быть дизенфекцией, но погибло
    # def is_disinfection(self):
    #     pass

    # ============================================

    # Для людей с огр. возможностями
    # Вход, оборудованный для инвалидов-колясочников
    def is_entrance_for_handicapped_people(self):
        try:
            return self.driver.find_element(By.XPATH, "//*[contains(@aria-label, 'оборудованный для инвалидов-колясочников')]").text
        except Exception:
            return "NotFound"

    #Предложения
    #Детское меню
    def is_menu_for_child(self):
        try:
            return self.driver.find_element(By.XPATH, "//*[contains(@aria-label, 'Has kids' menu')]").text
        except Exception:
            return "NotFound"

    def is_lunch(self):
        pass
    def is_supper(self):
        pass
    def is_desserts(self):
        pass
    def is_relaxed_atmosphere(self):
        pass
    def large_companies_people(self):
        pass
    def debit_cards(self):
        pass
    def is_closed(self):
        pass

    def is_dine_in(self):
        try:
            self.click_about()
            return bool(self.driver.find_element(By.XPATH, '//*[@aria-label="Serves dine-in"]').text)
        except Exception:
            # aria-label="No dine-in"
            return False
    def is_drive_through(self):
        try:
            self.click_about()
            return bool(self.driver.find_element(By.XPATH, "//*[contains(@aria-label, 'drive-through')]").text)
        except Exception:
            return False
    def is_average_rating(self):
        try:
            return self.driver.find_element(By.XPATH, "//*[contains(@jsaction, 'pane.reviewChart.moreReviews')]/div[2]/div[1]").text
        except Exception:
            return "NotFound"

    def is_number_of_reviews(self):
        try:
            return self.driver.find_element(By.XPATH, "//button[contains(@jsaction, 'pane.reviewChart.moreReviews')]").text
        except Exception:
            return "NotFound"

    def is_necessary_to_wear_a_mask(self):
        pass

    # $x('//span[contains(text(), "Temporarily closed")]')
    def temporarily_closed(self):
        try:
            return bool(self.driver.find_element(By.XPATH,
                                            '//span[contains(text(), "Temporarily closed")]'))
        except Exception:
            return "NotFound"


    # $x('//span[contains(text(), "Temporarily closed")]')
    def permanently_closed(self):
        try:
            return bool(self.driver.find_element(By.XPATH,
                                            '//span[contains(text(), "Permanently closed")]'))
        except Exception:
            return "NotFound"


    def run(self):
        time.sleep(5)
        # блок кода 1 странички
        self.name_building = self.get_name_building()
        print(f"name_building: {self.name_building}")
        self.address = self.get_address()
        print(f"address: {self.address}")
        self.post_code = self.get_post_code()
        print(f"post_code: {self.post_code}")
        self.city = self.get_city()
        print(f"city: {self.city}")
        time.sleep(1)
        self.plus_code = self.get_plus_code()
        print(f"plus_code: {self.plus_code}")
        self.time_work_days = self.get_time_work_days()
        print(f"time_work_days: {self.time_work_days}")
        # добавить выключить попап
        # self.delivery_sites = self.get_delivery_sites()
        # print(f"delivery_sites: {self.delivery_sites}")
        time.sleep(3)
        self.average_rating = self.is_average_rating()
        print(f"average_rating: {self.average_rating}")
        self.site = self.get_site()
        print(f"site: {self.site}")

        self.phone = self.get_phone()
        print(f"phone: {self.phone}")
        self.number_of_reviews = self.is_number_of_reviews()
        print(f"number_of_reviews: {self.number_of_reviews}")
        self.contactless_delivery = self.is_contactless_delivery()
        print(f"contactless_delivery: {self.contactless_delivery}")
        self.delivery = self.is_delivery()
        print(f"delivery: {self.delivery}")
        self.food_in_the_establishment = self.is_food_in_the_establishment()
        print(f"food_in_the_establishment: {self.food_in_the_establishment}")
        self.drive_through = self.is_drive_through()
        print(f"drive_through: {self.drive_through}")


        self.takeawey_food = self.is_takeawey_food()
        print(f"takeawey_food: {self.takeawey_food}")
        self.dine_in = self.is_dine_in()
        print(f"Dine in: {self.dine_in}")
        self.time_open, self.time_closing, self.time_interval = self.get_delta_work_time()
        print(f"time_open: {self.time_open}")
        print(f"time_closing: {self.time_closing}")
        print(f"time_interval: {self.time_interval}")
        self.geo_lat_long = self.get_geo_lat_long()
        print(f"geo_lat_long: {self.geo_lat_long}")
        self.temporarily_closed = self.temporarily_closed()
        print(f"temporarily_closed: {self.temporarily_closed}")

    def get(self):
    # Для некоторых данных возможно потребуется предподготовка
    # Например для списков (домены сайтов доставки)
        return pd.DataFrame({
                            'name': [self.name_building],
                            'address': [self.address],
                            'post_code': [self.post_code],
                            'city': [self.city],
                            'plus code':[self.plus_code],
                            'Lat/ long': [self.geo_lat_long],
                            'Lat': [self.geo_lat_long.split(",")[0]],
                            'long': [self.geo_lat_long.split(",")[1]],
                            'site': [self.site],
                            'phone': [self.phone],
                            "drive_through": [self.drive_through],
                            'contactless_delivery': [self.contactless_delivery],
                            'takeawey_food': [self.takeawey_food],
                            'dine_in': [self.dine_in],
                            'food_in_the_establishment': [self.food_in_the_establishment],
                            'delivery': [self.delivery],
                            'average_rating': [self.average_rating],
                            'number_of_reviews': [self.number_of_reviews],
                            'Monday': [self.time_work_days["Monday"]],
                            'Tuesday': [self.time_work_days["Tuesday"]],
                            'Wednesday': [self.time_work_days["Wednesday"]],
                            'Thursday': [self.time_work_days["Thursday"]],
                            'Friday': [self.time_work_days["Friday"]],
                            'Saturday': [self.time_work_days["Saturday"]],
                            'Sunday': [self.time_work_days["Sunday"]],
                            'Monday open': [self.time_open["Monday"]],
                            'Tuesday open': [self.time_open["Tuesday"]],
                            'Wednesday open': [self.time_open["Wednesday"]],
                            'Thursday open': [self.time_open["Thursday"]],
                            'Friday open': [self.time_open["Friday"]],
                            'Saturday open': [self.time_open["Saturday"]],
                            'Sunday open': [self.time_open["Sunday"]],
                            'Monday closing': [self.time_closing["Monday"]],
                            'Tuesday closing': [self.time_closing["Tuesday"]],
                            'Wednesday closing': [self.time_closing["Wednesday"]],
                            'Thursday closing': [self.time_closing["Thursday"]],
                            'Friday closing': [self.time_closing["Friday"]],
                            'Saturday closing': [self.time_closing["Saturday"]],
                            'Sunday closing': [self.time_closing["Sunday"]],
                            'Monday delta': [self.time_interval["Monday"]],
                            'Tuesday delta': [self.time_interval["Tuesday"]],
                            'Wednesday delta': [self.time_interval["Wednesday"]],
                            'Thursday delta': [self.time_interval["Thursday"]],
                            'Friday delta': [self.time_interval["Friday"]],
                            'Saturday delta': [self.time_interval["Saturday"]],
                            'Sunday delta': [self.time_interval["Sunday"]],
                            'url': [self.url],
                            'Permanently closed': [],
                             })




    # url1 = "https://www.google.ru/maps/place/KFC+Bury/@53.5762876,-2.2760582,17z/data=!4m9!1m2!2m1!1sKFCCosta+Coffee+Drive+Thru,+Park+66+Bury+Bury+Greater+Manchester+BL9+8RZ!3m5!1s0x487ba5bf3eb2920f:0x97a6046ff31e9d96!8m2!3d53.5763074!4d-2.2739022!15sCkhLRkNDb3N0YSBDb2ZmZWUgRHJpdmUgVGhydSwgUGFyayA2NiBCdXJ5IEJ1cnkgR3JlYXRlciBNYW5jaGVzdGVyIEJMOSA4UlpIiIibofqvgIAIWkkiR2tmY2Nvc3RhIGNvZmZlZSBkcml2ZSB0aHJ1IHBhcmsgNjYgYnVyeSBidXJ5IGdyZWF0ZXIgbWFuY2hlc3RlciBibDkgOHJ6YgkJTtdWJVWDX0aSARRmYXN0X2Zvb2RfcmVzdGF1cmFudJoBI0NoWkRTVWhOTUc5blMwVkpRMEZuU1VOTGJqWmllV1ozRUFF"
    # url2 = "https://www.google.ru/maps/place/Greggs/@55.8364478,-4.2667374,17z/data=!4m13!1m7!3m6!1s0x488846f24156e0c3:0x288d289050d9b867!2sGreggs!8m2!3d55.8364478!4d-4.2645487!10e1!3m4!1s0x488846f24156e0c3:0x288d289050d9b867!8m2!3d55.8364478!4d-4.2645487"
    # url3 = "https://www.google.co.uk/maps/place/Pret+A+Manger/@52.4820496,-1.900123,17z/data=!3m1!4b1!4m5!3m4!1s0x4870bc8e59100879:0x698e05f2ebac13e5!8m2!3d52.4820496!4d-1.8979343?authuser=0&hl=en"
    # url4 = "https://www.google.ru/maps/place/McDonald's/@54.6471675,-5.6605121,17z/data=!3m1!4b1!4m5!3m4!1s0x486175f130240c87:0x7ca6d978ccb9aa1f!8m2!3d54.6470922!4d-5.6582704"
    # url5 = "https://www.google.ru/maps/place/KFC+London/@51.5161673,-0.1765175,17z/data=!4m13!1m7!3m6!1s0x48761ab2e6f6a799:0xfea42139dd6b42b5!2sKFC+London!8m2!3d51.5161673!4d-0.1743288!10e2!3m4!1s0x48761ab2e6f6a799:0xfea42139dd6b42b5!8m2!3d51.5161673!4d-0.1743288"
    #
    # for i in [url1, url2, url3, url4, url5]:
    #     ParseGoogle(i).get()

    # a = ParseGoogle(url5).get().to_excel("123.xlsx")
    # print(tabulate(ParseGoogle(url1).get()))
    #
def parse(file_name):
    try:
        print(file_name)
        for i in file_name:
            temp_pd_df = []
            urls = [j for j in pd.read_excel(f"{i}")["source"]]
            for url in urls:
                try:
                    print(url)
                    temp = ParseGoogle(url)
                    temp_pd_df.append(temp.get())

                except Exception as ex:
                    print(ex)
                    temp_pd_df.append(pd.DataFrame({
                                                    'name': ["NotFound"],
                                                    'address': ["NotFound"],
                                                    'post_code': ["NotFound"],
                                                    'city': ["NotFound"],
                                                    'Lat/ long': ["NotFound"],
                                                    'site': ["NotFound"],
                                                    'phone': ["NotFound"],
                                                    'contactless_delivery': ["NotFound"],
                                                    'takeawey_food': ["NotFound"],
                                                    'food_in_the_establishment': ["NotFound"],
                                                    'delivery': ["NotFound"],
                                                    'average_rating': ["NotFound"],
                                                    'number_of_reviews': ["NotFound"],
                                                    'Monday': ["NotFound"],
                                                    'Tuesday': ["NotFound"],
                                                    'Wednesday': ["NotFound"],
                                                    'Thursday': ["NotFound"],
                                                    'Friday': ["NotFound"],
                                                    'Saturday': ["NotFound"],
                                                    'Sunday': ["NotFound"],
                                                    'Monday open': ["NotFound"],
                                                    'Tuesday open': ["NotFound"],
                                                    'Wednesday open': ["NotFound"],
                                                    'Thursday open': ["NotFound"],
                                                    'Friday open': ["NotFound"],
                                                    'Saturday open': ["NotFound"],
                                                    'Sunday open': ["NotFound"],
                                                    'Monday closing': ["NotFound"],
                                                    'Tuesday closing': ["NotFound"],
                                                    'Wednesday closing': ["NotFound"],
                                                    'Thursday closing': ["NotFound"],
                                                    'Friday closing': ["NotFound"],
                                                    'Saturday closing': ["NotFound"],
                                                    'Sunday closing': ["NotFound"],
                                                    'Monday delta': ["NotFound"],
                                                    'Tuesday delta': ["NotFound"],
                                                    'Wednesday delta': ["NotFound"],
                                                    'Thursday delta': ["NotFound"],
                                                    'Friday delta': ["NotFound"],
                                                    'Saturday delta': ["NotFound"],
                                                    'Sunday delta': ["NotFound"],
                                                    'url': [url],
                                                    'Permanently closed': ["NotFound"],
                                                     }))
                finally:
                    continue
            pd.concat(temp_pd_df).to_excel(f"{i[:-5]} result.xlsx")
        return None
    except:
        return None
if __name__ == '__main__':
    file_name = [ 'doparsit.xlsx',]

    a = [[i] for i in file_name]

    with Pool(processes=1) as p:
        p.map(parse, a)

