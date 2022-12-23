import time

from parsers.website.promo.uber_eats.uber_eats import UberEatsPromoParser

from datetime import datetime
import pandas as pd

from database.database import DataBase

class UberEatsPromoController():

        def __init__(self):
                self.get_search_row()
                self.data_for_search = self.get_search_row()
                print(self.data_for_search)
                self.start_parse()


        def get_search_row(self):
                rows = DataBase().get_table('uber_eats_promo_search_data')
                data_for_search = []

                for row in next(rows):
                        data_for_search.append(row)
                return pd.concat(data_for_search)

        def start_parse(self):
                for _, (post_code, city) in self.data_for_search.iterrows():
                        with UberEatsPromoParser(post_code=post_code) as parser:
                                for index in range(len(parser.cards)):
                                        date = datetime.now().strftime("%d.%m.%Y")
                                        data = {
                                                'get_html': parser.get_html(index),
                                                'get_image': parser.get_image(index),
                                                'get_head': parser.get_head(index),
                                                'get_description': parser.get_description(index),
                                                'get_prices': parser.get_prices(index),
                                                'get_times': parser.get_times(index),
                                                'get_rating': parser.get_rating(index),
                                                'post_code': post_code,
                                                'city': city,
                                                'date': date,
                                        }
                                        print(data)
                                        self.to_stg_db(pd.DataFrame(data, index=[0]), 'UBEREATS_PROMO_HTML_CARDS')



        def to_stg_db(self, data_frame, name_stg_table):
                DataBase().to_stg_table(data_frame=data_frame, name_stg_table=name_stg_table)



