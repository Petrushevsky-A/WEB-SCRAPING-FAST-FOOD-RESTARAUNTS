from pathlib import Path




DATABASES = {
    'host': 'localhost:5432',
    'user': 'postgres',
    'password': 'postgres',
    'database': 'scraping_reustaran',
}


PROXY_SELENIUMWIRE = {
    'proxy': {
        # irland
        # 'http': f'http://5AcmYPMAn:fLydRaWbd@91.239.213.181:63184',
        # 'https': f'https://5AcmYPMAn:fLydRaWbd@91.239.213.181:63184',

        # uk 196.18.165.20
        # qXkJ97
        # UjNPey
        # 8000
        'http': f'http://qXkJ97:UjNPey@196.18.165.20:8000',
        'https': f'https://qXkJ97:UjNPey@196.18.165.20:8000',
    }
}


SELENIUM = {
    'browser_type': {
                        True: 'chrome',
                        False: 'yandex',
                        False: 'opera',
                        False: 'safari',
                        False: 'ie',
                        False: 'edge',
                     }[True],
    # 'path': Path.cwd() / r'chromedriver',
    'path': Path.cwd() / r'yandexdriver',
    # 'path': Path.cwd() / r'geckodriver',
    'options':
        {
            # 'sandbox': '--no-sandbox',
            # 'headless':'--headless',
            # 'shm': '--disable-dev-shm-usage',
            # 'user-agent':"user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.99 Safari/537.36",
            'user-agent':"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
            # 'automation_controlled':"--disable-blink-features=AutomationControlled",
            'windows_size' :"--start-maximized",
            'language' :"--lang=en-nz",
            # 'certificate-errors': '--ignore-certificate-errors',
            # 'ssl': '--ignore-ssl-errors=yes',
        }
}

EXPERIMENTAL_OPTION_SELENIUM = {
    'excludeSwitches': ["enable-automation"],
    'useAutomationExtension': False,
}

PARSER = {
    'NUMBER_ATTEMPTS': 1,

    # seconds
    'TIMEOUT_SCRIPT': 10*60,
}



APPS = {
        'platformName':'Android',
        'platformVersion': '8.1',
        'deviceName': 'Pixel_3a_API_33_x86_64',
        'udid': 'emulator-5554',
        # 'app': (r'/home/oem/PycharmProjects/MeaningfulVision_Webscaping/McDonald’s UK_v7.4.4_apkpure.com.apk'),
    }


APPIUM = {
    'url': r'http://127.0.0.1:4723/wd/hub',
    'path_emulator': r'/home/oem/Android/Sdk/tools',
    'commands_run_emulator':'',
}
