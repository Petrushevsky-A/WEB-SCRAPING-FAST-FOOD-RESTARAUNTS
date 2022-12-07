from parsers.promo.dominos.dominos import DominosPromoParser
from database.database import DataBase

import time
from datetime import datetime

from itertools import repeat
import pandas as pd

class DominosPromoController():

    def __init__(self):

        url = 'https://www.dominos.co.uk/'

        post_codes = [
            'W1C 1LX',
            'CF10 1PN',
            'BT1 5AA',
            'G1 3SQ',
            'B2 4QA',
            'L1 8JQ',
            'LS1 1UR',
            'M2 5DB',
        ]

        for post_code in post_codes:
            self.start_parse(post_code)

    def start_parse(self, post_code):
        try:
            with DominosPromoParser(post_code = post_code) as parser:
                collumns = (
                    'date',
                    'html_cards',
                    'voucher',
                    'collect_deals',
                    'image',
                    'post_code',
                    'address',
                    'index',
                )
                date = datetime.now().strftime("%d.%m.%Y")

                gen_vouchers = parser.get_vouchers()

                data_vouchers = list(zip(
                    repeat(date),
                    repeat('Not found'),
                    gen_vouchers,
                    repeat('Not found'),
                    repeat('Not found'),
                    repeat(post_code),
                    repeat(parser.address),
                    repeat(-1),
                ))

                for row in data_vouchers:
                    voucher = dict(zip(collumns, row))

                    # print(voucher)
                    df_voucher = pd.DataFrame(data=voucher, index=[0])
                    # print(df_voucher)
                    self.to_stg_db(df_voucher, 'stg_dominos_promo')


                count_cards = parser.get_count_cards_deals_2()
                print(count_cards)
                for index in range(count_cards):
                    parser.scrolling_page(index)

                    type_card = parser.get_type_card(index)
                    print(type_card,f' index {index}')
                    time.sleep(0.1)
                    try:
                        get_data = {
                            'common_type': parser.get_collect_deals_2,
                            'button_type': parser.get_button_collect_deals,
                        }[type_card](index)

                        collumns = (
                            'date',
                            'html_cards',
                            'voucher',
                            'collect_deals',
                            'image',
                            'post_code',
                            'address',
                            'index',
                        )
                        date = datetime.now().strftime("%d.%m.%Y")

                        # gen_collect_deals = parser.get_collect_deals_(index)
                        image_deals = parser.get_cards_tray_image()

                        data_collect_deals = list(zip(
                            repeat(date),  # date
                            repeat('Not found'),  # html_cards
                            repeat('Not found'),  # voucher
                            get_data,  # collect_deals
                            repeat('Not found'),  # image
                            # parser.cards_tray_image,  # image
                            repeat(post_code),  # post_code
                            repeat(parser.address),  # address
                            repeat(index),  # index
                        ))
                        print(123)
                        for row in data_collect_deals:
                            deals = dict(zip(collumns, row))

                            print(deals)
                            df_deals = pd.DataFrame(data=deals, index=[0])
                            print(df_deals)
                            self.to_stg_db(df_deals, 'stg_dominos_promo')
                        parser.cards_tray_image = ['Not found', ]
                    except Exception as ex:
                        print(ex)
                        # print(123)
                        pass

                else:
                    time.sleep(3)







        except Exception as ex:
            print(ex)
            # time.sleep(3333)


    def get_address(self, parser = None):
        if parser:
            address = parser.get_address()
            post_code = parser.post_code
            date = datetime.now().strftime("%d.%m.%Y")

            data = {
                    'address': address,
                    'post_code': post_code,
                    'date': date,
                    }
            html_card = pd.DataFrame(data=data, index=[0])
            self.to_stg_db(html_card, 'STG_DOMINOS_INFO')







    def to_stg_db(self, data_frame, name_stg_table):
        DataBase().to_stg_table(data_frame= data_frame, name_stg_table=name_stg_table)
