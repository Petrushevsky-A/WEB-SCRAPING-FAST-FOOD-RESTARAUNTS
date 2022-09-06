import time

from parsers.promo.hotukdeals.hotukdeals import HotukdealsParser
from cleaner.hotukdeals.hotukdeals import HotukdealsCleaner
from database.database import DataBase


class HotukdealsController():

    def __init__(self):
        # self.start_parse()
        print(self.get_urls_voucher_codes_page())
        print(self.get_urls_deals_cards_page())
        # self.parsed_deals_cards_page()
        # self.parsed_voucher_codes_page()

    def start_parse(self):
        # Возращает в бд html карточек
        url = 'https://www.hotukdeals.com/vouchers/burgerking.co.uk'
        with HotukdealsParser(url = url) as parser:
            parser.click_voucher_codes()
            time.sleep(1)
            self.scrolling_voucher_codes_page(parser)
            time.sleep(1)
            data_voucher = parser.get_voucher_codes_cards()
            self.to_stg_db(data_voucher, 'STG_HOTUKDEALS_BURGERKING_VOUCHER_CODES_CARDS')
            time.sleep(2)
            parser.click_deals()
            time.sleep(1)
            self.scrolling_deals_cards_page(parser)
            time.sleep(1)
            data_deals = parser.get_deals_cards()
            self.to_stg_db(data_deals, 'STG_HOTUKDEALS_BURGERKING_DEALS_CARDS')
            time.sleep(2)


    def get_urls_deals_cards_page(self):
        html_voucher_codes = DataBase().get_table('STG_HOTUKDEALS_BURGERKING_DEALS_CARDS')
        print('Deals')
        urls = []
        for row in html_voucher_codes['deals_card']:
            urls.append(HotukdealsCleaner(data_html=row).get_url_deals_page()[0])
        return urls

    def get_urls_voucher_codes_page(self):
        html_voucher_codes = DataBase().get_table('STG_HOTUKDEALS_BURGERKING_VOUCHER_CODES_CARDS')
        print('Voucher codes')
        urls = []
        for row in html_voucher_codes['voucher_codes_card']:
            urls.append(HotukdealsCleaner(data_html=row).get_url_voucher_page()[0])
        return urls

    def parsed_voucher_codes_page(self):
        urls = self.get_urls_voucher_codes_page()
        with HotukdealsParser(url=urls[0]) as parser:
            for url in urls:
                time.sleep(2)
                parser.open_url(url)
                time.sleep(2)
                data = parser.get_voucher_codes_page()
                time.sleep(2)
                self.to_stg_db(data, 'STG_BURGERKING_DEALS_VOUCHER_CODES_PAGE')
                time.sleep(2)


    def parsed_deals_cards_page(self):
        urls = self.get_urls_deals_cards_page()
        with HotukdealsParser(url=urls[0]) as parser:
            for url in urls:
                time.sleep(2)
                parser.open_url(url)
                time.sleep(2)
                data = parser.get_deals_page()
                time.sleep(2)
                self.to_stg_db(data, 'STG_BURGERKING_DEALS_CARDS_PAGE')
                time.sleep(2)

    def to_stg_db(self, data_frame, name_stg_table):
        # DataBase().create_stg_table(data_frame= self.get_deals_cards, name_stg_table='STG_HOTUKDEALS_BURGERKING')
        DataBase().create_stg_table(data_frame= data_frame, name_stg_table=name_stg_table)

    def scrolling_voucher_codes_page(self, parser):
        parser.see_more_voucher_codes_page()
        time.sleep(2)
        parser.see_more_voucher_codes_page()
        time.sleep(2)
        parser.see_more_voucher_codes_page()
        time.sleep(2)

    def scrolling_deals_cards_page(self, parser):
        parser.see_more_deals_cards_page()
        time.sleep(2)
        parser.see_more_deals_cards_page()
        time.sleep(2)
        parser.see_more_deals_cards_page()
        time.sleep(2)