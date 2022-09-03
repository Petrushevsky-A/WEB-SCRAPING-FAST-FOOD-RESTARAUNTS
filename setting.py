
DATABASES = {
    'host': 'localhost',
    'user': 'root',
    'password': '12758698',
    'database': 'parser_fastfood',

    # Dict тип данных независим от позиции полей, поэтому
    # 'cursorclass': pymysql.cursors.DictCursor,
}


SELENIUM = {
    'path': r'chromedriver.exe',
    'options':
        {
            'user-agent':"user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.5195.52 Safari/537.36",
            'automation_controlled':"--disable-blink-features=AutomationControlled",
            'windows_size' :"--start-maximized",
            'language' :"--lang=en-nz",
        }
}