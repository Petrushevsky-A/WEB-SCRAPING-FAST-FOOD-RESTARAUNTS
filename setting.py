from pathlib import Path

DATABASES = {
    'host': 'localhost:5432',
    'user': 'postgres',
    'password': 'root',
    'database': 'fastfood_parser',

    # Dict тип данных независим от позиции полей, поэтому
    # 'cursorclass': pymysql.cursors.DictCursor,
}


SELENIUM = {
    # 'path': r'chromedriver.exe',
    'path': Path.cwd() / r'chromedriver.exe',
    'options':
        {
            'user-agent':"user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.71 Safari/537.36",
            'automation_controlled':"--disable-blink-features=AutomationControlled",
            'windows_size' :"--start-maximized",
            'language' :"--lang=en-nz",
        }
}