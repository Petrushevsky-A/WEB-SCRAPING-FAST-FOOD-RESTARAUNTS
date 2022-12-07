import time

import pandas as pd
import requests
import itertools

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from datetime import datetime

from database.database import DataBase
from itertools import repeat



from parsers.promo.uber_eats.uber_eats_2 import UberEatsPromoParser

class UberEatsPromoController():

        def __init__(self):
                self.get_search_row()
                self.data_for_search = self.get_search_row()
                print(self.data_for_search)

        # def get_search_row(self):
        #         rows = DataBase().get_table('uber_eats_list_url')
        #         data_for_search = []
        #
        #         for row in next(rows):
        #                 data_for_search.append(row)
        #         return pd.concat(data_for_search)

        def get_search_row(self):
                rows = DataBase().get_table('uber_eats_promo_search_data')
                data_for_search = []

                for row in next(rows):
                        data_for_search.append(row)
                return pd.concat(data_for_search)

        def start_parse(self):
                for _, (post_code, city) in self.data_for_search.iterrows():
                        with UberEatsPromoParser(post_code=post_code) as parser:
                                pass
                        for index in range(len(parser.cards)):
                                date = datetime.now().strftime("%d.%m.%Y")

                                data = {
                                        'get_html': parser.get_html(index),
                                        'get_image': parser.get_image(index),
                                        'get_alt_image': parser.get_alt_image(index),
                                        'get_head': parser.get_head(index),
                                        'get_alt_head': parser.get_alt_head(index),
                                        'get_description': parser.get_description(index),
                                        'get_alt_description': parser.get_alt_description(index),
                                        'get_prices': parser.get_prices(index),
                                        'get_alt_prices': parser.get_alt_prices(index),
                                        'get_times': parser.get_times(index),
                                        'get_alt_times': parser.get_alt_times(index),
                                        'get_rating': parser.get_rating(index),
                                        'get_alt_rating': parser.get_alt_rating(index),
                                        'post_code': post_code,
                                        'city': city,
                                        'date': date,
                                }
                                self.to_stg_db(pd.DataFrame(data), 'UBEREATS_PROMO_HTML_CARDS')



        def to_stg_db(self, data_frame, name_stg_table):
                # DataBase().create_stg_table(data_frame= self.get_deals_cards, name_stg_table='STG_HOTUKDEALS_BURGERKING')
                DataBase().to_stg_table(data_frame=data_frame, name_stg_table=name_stg_table)




