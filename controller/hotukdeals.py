import time

from parsers.promo.hotukdeals.hotukdeals import HotukdealsParser
from cleaner.hotukdeals.hotukdeals import HotukdealsCleaner
from database.database import DataBase


class HotukdealsController():

    def __init__(self):
        # self.start_parse()
        # self.get_urls_voucher_codes_page()
        # self.get_urls_deals_cards_page()
        # self.parsed_deals_cards_page()
        self.parsed_voucher_codes_page()

    def start_parse(self):
        # Возращает в бд html карточек
        url = 'https://www.hotukdeals.com/vouchers/burgerking.co.uk'
        with HotukdealsParser(url = url) as parser:
            parser.click_voucher_codes()
            time.sleep(1)
            data_voucher = parser.get_voucher_codes_cards()
            self.to_stg_db(data_voucher, 'STG_HOTUKDEALS_BURGERKING_VOUCHER_CODES_CARDS')
            time.sleep(1)
            data_deals = parser.get_deals_cards()
            self.to_stg_db(data_deals, 'STG_HOTUKDEALS_BURGERKING_DEALS_CARDS')
            time.sleep(2)
            parser.click_deals()
            time.sleep(2)


    def get_urls_deals_cards_page(self):
        html_voucher_codes = DataBase().get_table('STG_HOTUKDEALS_BURGERKING_DEALS_CARDS')
        print('Deals')
        urls = []
        for row in html_voucher_codes['deals_card']:
            urls.append(HotukdealsCleaner().get_url_deals_page(row)[0])
        return urls

    def get_urls_voucher_codes_page(self):
        html_voucher_codes = DataBase().get_table('STG_HOTUKDEALS_BURGERKING_VOUCHER_CODES_CARDS')
        print('Voucher codes')
        urls = []
        for row in html_voucher_codes['voucher_codes_card']:
            url = HotukdealsCleaner().get_url_voucher_page(row)[0]
            if not 'visit' in url:
                urls.append(url)
        return urls

    def parsed_voucher_codes_page(self):
        urls = self.get_urls_voucher_codes_page()
        # print(urls[0])
        # print(type(urls[0]))
        with HotukdealsParser(url=urls[0]) as parser:
            for url in urls:
                time.sleep(2)
                parser.get_voucher_codes_page()
                time.sleep(2)
                parser.open_url(url)
                time.sleep(2)

    def parsed_deals_cards_page(self):
        urls = self.get_urls_deals_cards_page()
        with HotukdealsParser(url=urls[0]) as parser:
            for url in urls:
                time.sleep(2)
                parser.get_deals_page()
                time.sleep(2)
                parser.open_url(url)
                time.sleep(2)

    def to_stg_db(self, data_frame, name_stg_table):
        # DataBase().create_stg_table(data_frame= self.get_deals_cards, name_stg_table='STG_HOTUKDEALS_BURGERKING')
        DataBase().create_stg_table(data_frame= data_frame, name_stg_table=name_stg_table)