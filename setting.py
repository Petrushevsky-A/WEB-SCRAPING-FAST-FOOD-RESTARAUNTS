from pathlib import Path


OS = {
    True:'Linux',
    False:'Windows',
}


DATABASES = {
    'host': 'localhost:5432',
    'user': 'postgres',
    'password': 'postgres',
    'database': 'scraping_reustaran',
}

# London ip4
PROXY = {
    'PROXY_HOST': '196.18.165.20',
    'PROXY_PORT': '8000',
    'PROXY_USER': 'qXkJ97',
    'PROXY_PASS': 'UjNPey',
}

# Dublin ip4
# PROXY = {
# 'PROXY_HOST': '91.239.213.181',
# 'PROXY_PORT': '63184',
# 'PROXY_USER': '5AcmYPMAn',
# 'PROXY_PASS': 'fLydRaWbd',
# }

SELENIUM = {
    'path': Path.cwd() / r'chromedriver',
    # 'path': Path.cwd() / r'yandexdriver',
    # 'path': Path.cwd() / r'geckodriver',
    'options':
        {
            # 'sandbox': '--no-sandbox',
            # 'headless':'--headless',
            # 'shm': '--disable-dev-shm-usage',
            # 'user-agent':"user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.99 Safari/537.36",
            # 'user-agent':"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
            'user-agent':"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.124 Safari/537.36",
            'automation_controlled':"--disable-blink-features=AutomationControlled",
            'windows_size' :"--start-maximized",
            'language' :"--lang=en-nz",
            # 'certificate-errors': '--ignore-certificate-errors',
            # 'ssl': '--ignore-ssl-errors=yes',
            # 'proxy':'--proxy-server=196.18.165.20:8000',
        },
    'extension': {
        'path_proxy_plugin_file': Path.cwd() / r'proxy_auth_plugin.zip',
    },
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

CONCURRENCY = 5