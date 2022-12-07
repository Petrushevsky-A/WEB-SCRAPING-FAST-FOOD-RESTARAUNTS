from parsers.price.dominos.dominos import DominosParser
from database.database import DataBase

from itertools import repeat

import time
from datetime import datetime

import pandas as pd


class DominosController():

    def __init__(self):

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
        with DominosParser(post_code = post_code) as parser:
            count_cards = parser.get_count_cards()
            for index in range(count_cards):
                print(f'index {index}')

                type_card = parser.get_type_card(index)
                print(type_card)

                get_html = {
                                'common_type': parser.scrolling_common,
                                'select_type': parser.scrolling_select,
                                'choose_type': parser.scrolling_choose,
                            }[type_card](index)
                get_category = parser.get_category(index)

                collumns = (
                    'html_card',
                    'select',
                    'date_parse',
                    'post_code',
                    'index_card',
                    'category',
                    'image',
                    'price',
                    'name',
                    'type_card',
                )
                date = datetime.now().strftime("%d.%m.%Y")

                image = parser.get_image(index)
                price = parser.get_price(index)
                name = parser.get_name(index)
                option_select = parser.option_text
                for row in zip(
                                get_html,
                                option_select,
                                repeat(date),
                                # change
                                repeat(post_code),
                                repeat(index),
                                repeat(get_category),
                                repeat(image),
                                repeat(price),
                                repeat(name),
                            ):
                    data = dict(zip(collumns, (*row, type_card)))
                    print(data)
                    html_card = pd.DataFrame(data=data, index=[0])
                    self.to_stg_db(html_card, 'STG_DOMINOS_HTML_CARDS')
                parser.option_text = ['Not found']
                parser.scrolling_page(index)
            else:
                print('finaly parsed')
            # self.get_address(parser, post_code)



    def get_address(self, parser = None, post_code_for_search = 'Not faund',city='Not found'):
        if parser:
            address = parser.get_address()
            post_code = parser.post_code
            date = datetime.now().strftime("%d.%m.%Y")

            data = {
                    'address': address,
                    'post_code': post_code,
                    'date': date,
                    'city':city,
                    'post_code_for_search':post_code_for_search,
                    }
            html_card = pd.DataFrame(data=data, index=[0])
            self.to_stg_db(html_card, 'DIM_DOMINOS_INFO')



    def to_stg_db(self, data_frame, name_stg_table):
        DataBase().to_stg_table(data_frame= data_frame, name_stg_table=name_stg_table)

    def scrolling_page(self, parser):
        parser.see_more_voucher_codes_page()
        time.sleep(2)