from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import undetected_chromedriver.v2 as undetected_chrome


import time
import setting


class GmailParsePromo():
    def __init__(self):
        self.driver = None

    def __enter__(self):
        self.run_browser()
        time.sleep(2)
        self.open_url()
        time.sleep(2)
        self.accept_click()
        time.sleep(2)
        self.authorization()
        time.sleep(2)
        self.to_all_mail()
        time.sleep(2)
        number_list = 0
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.close()
        self.driver.quit()

    def run_browser(self):
        options = Options()
        tuple(map(options.add_argument, setting.SELENIUM['options'].values()))
        options.add_extension(setting.SELENIUM['extension']['path_proxy_plugin_file'])
        print(setting.SELENIUM['extension']['path_proxy_plugin_file'])
        time.sleep(1)

        self.driver = undetected_chrome.Chrome(option=options)
        self.driver.delete_all_cookies()

    def open_url(self):
        url = 'https://www.google.com/gmail/about/'
        self.driver.get(url)
        time.sleep(5)

    def authorization(self):
        MAIL = 'fastfoodlondon2021@gmail.com'
        PASSWORD = 'Projectplaner123'

        try:
            self.driver.find_element(By.XPATH, '//a[contains(text(), "Sign")]').click()
            time.sleep(2)
        except:
            self.driver.find_element(By.XPATH, '//a[contains(text(), "Войти")]').click()
            time.sleep(2)

        self.driver.find_element(By.XPATH, '//input[@type="email"]').send_keys(MAIL)
        time.sleep(1)
        self.driver.find_element(By.XPATH, '//input[@type="email"]').send_keys(Keys.ENTER)
        time.sleep(2)

        self.driver.find_element(By.XPATH, '//input[@type="password"]').send_keys(PASSWORD)
        time.sleep(1)
        self.driver.find_element(By.XPATH, '//input[@type="password"]').send_keys(Keys.ENTER)
        time.sleep(2)

    def accept_click(self):
        try:
            self.driver.find_element(By.XPATH, '//a[contains(text(), "OK")]').click()
        except:
            pass

    def to_all_mail(self):
        url = 'https://mail.google.com/mail/u/2/?ogbl#all'
        self.driver.get(url)
        time.sleep(4)

    def get_count_messages(self):
        try:
            xpath = r'//div[@class="AO"]//tr'
            messages = self.driver.find_elements(By.XPATH, xpath)
            count_message = len(messages)
        except:
            print('except count messages')
            count_message = 50
        finally:
            return count_message



    def get_head(self):
        try:
            xpath = r'//h2[@data-legacy-thread-id]'
            head = self.driver.find_element(By.XPATH, xpath).text
        except:
            head = 'Not Found'
        finally:
            return head

    def get_image(self):
        try:
            xpath = r'//div[@id and @jslog][.//u]//img'
            image = [i.get_attribute('src') for i in
                     self.driver.find_elements(By.XPATH, xpath)]
            image = ', '.join(image)
        except:
            image = 'Not Found'
        finally:
            return image

    def get_description(self):
        try:
            xpath = r'//div[@id and @jslog][.//u]'
            text = self.driver.find_element(By.XPATH, xpath).get_attribute('textContent')
        except:
            text = 'Not Found'
        finally:
            return text


    def get_hash_id(self):
        try:
            hash_id = self.driver.current_url.split('/')[-1]
        except:
            hash_id = 'Not Found'
        finally:
            return hash_id

    def get_html_message(self):
        try:
            xpath = r'//div[@id and @jslog][.//u]'
            html = self.driver.find_element(By.XPATH, xpath).get_attribute('outerHTML')
        except:
            print('Except get_html_message')
            html = 'Not Found'
        finally:
            return html

    def open_message(self, number):
        xpath = rf'(//div[@class="AO"]//tr)[{number}]'
        message = self.driver.find_element(By.XPATH, xpath)
        try:
            self.driver.execute_script("arguments[0].click();", message)
        except:
            message.click()
            message.click()
        time.sleep(7)

    def navigate_back(self):
        try:
            self.driver.back()
            time.sleep(4)
        except:
            self.to_all_mail()
