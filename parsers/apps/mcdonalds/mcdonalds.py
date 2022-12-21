import setting

import time

from datetime import datetime

from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy



class McDonaldsAppParser():

    def __init__(self):
        self.driver = None


    def __enter__(self):
        self.emulator_run()
        time.sleep(4)
        self.open_list_category()
        return self


    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_emulator()
        # self.open_list_category()

    def run_emulator(self):
        '''

        sudo adb kill-server
        sudo adb start-server
         ./emulator -avd Pixel_3a_API_33_x86_64

        :return:
        '''
        pass

    def emulator_run(self):
        url_apk_file = {'app': r'/home/oem/PycharmProjects/MeaningfulVision_Webscaping/McDonald’s UK_v7.4.4_apkpure.com.apk'}
        self.driver = webdriver.Remote(setting.APPIUM['url'], {**setting.APPS, **url_apk_file})


    def open_list_category(self):
        xpath = ''
        try:
            # xpath = r'//android.widget.TextView[@content-desc="Log in button"]'
            # time.sleep(3)
            # el = self.driver.find_element(by=AppiumBy.XPATH,
            #                               value=xpath)
            # el.click()
            # time.sleep(4)


            xpath = r'//android.widget.ImageView[@content-desc="Close"]'
            el = self.driver.find_element(by=AppiumBy.XPATH, value=xpath)
            el.click()
            time.sleep(5)


            ui_automator = 'new UiScrollable(new UiSelector().scrollable(true).instance(0)).scrollIntoView(new UiSelector().text("Start an order").instance(0));'
            self.driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR,ui_automator)
            xpath = r'//android.widget.TextView[@content-desc="Start an order button"]'
            el = self.driver.find_element(by=AppiumBy.XPATH, value=xpath)
            el.click()

            time.sleep(3)
            xpath = r'//android.widget.ImageView[@content-desc="Close"]'
            el = self.driver.find_element(by=AppiumBy.XPATH, value=xpath)
            el.click()
            time.sleep(6)

            xpath = r'//android.widget.ImageView[@content-desc="Search icon"]'
            el = self.driver.find_element(by=AppiumBy.XPATH, value=xpath)
            el.click()
            time.sleep(4)

            xpath = r'//android.widget.EditText'
            el = self.driver.find_element(by=AppiumBy.XPATH, value=xpath).send_keys('London')
            time.sleep(1)
            self.driver.long_press_keycode(66)
            time.sleep(5)

            xpath = r'//android.widget.TextView[@content-desc="Order Here, 34/35 STRAND, button"]'
            el = self.driver.find_element(by=AppiumBy.XPATH, value=xpath)
            el.click()
            time.sleep(6)
        except Exception as ex:
            print(xpath)
            print(ex)
        # xpath = r'/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/androidx.drawerlayout.widget.DrawerLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.RelativeLayout/android.widget.RelativeLayout/android.view.ViewGroup/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.ScrollView/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.view.ViewGroup[1]/android.widget.TextView'
        # el = self.driver.find_element(by=AppiumBy.XPATH, value=xpath)
        # el.click()
        # time.sleep(6)
        #
        # xpath = r'//android.widget.TextView[@content-desc="£6.39  3530 kJ/845 kcal "]'
        # el = self.driver.find_element(by=AppiumBy.XPATH, value=xpath)
        # print(el.text)
        # time.sleep(6)

    def get_category(self):
        '''
        /hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/androidx.drawerlayout.widget.DrawerLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.RelativeLayout/android.widget.RelativeLayout/android.view.ViewGroup/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.ScrollView/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.view.ViewGroup[3]

        /hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/androidx.drawerlayout.widget.DrawerLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.RelativeLayout/android.widget.RelativeLayout/android.view.ViewGroup/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/android.view.ViewGroup/androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup[2]
        :return:
        '''

        # //*[contains(@text, "menu")]/parent::android.widget.LinearLayout//android.view.ViewGroup

        pass





    def close_emulator(self):
        self.driver.close()
        self.driver.quit()