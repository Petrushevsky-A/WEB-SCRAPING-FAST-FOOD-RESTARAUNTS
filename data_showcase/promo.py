from datetime import datetime

import pandas as pd

from database.database import DataBase

class DeliverooPromoToPromoDB():
    def __init__(self):
        data = DataBase().get_table('stg_deliveroo_promo')
        for df in next(data):
            df.apply(self.convert, axis=1)


    def convert(self, row: pd.Series):
        data = {
            'start_date': row['date'],
            'end_date': row['date'],
            'brand': 'deliveroo',
            'segment': '',
            'city': row['city'],
            'postcode': row['post_code'],
            'title': row['name'],
            'promo_description_1_8': row['promotion'],
            'promo_type': '',
            'promo_type_edited': '',
            'app_in_store': '',
            'promo_title_edited': '',
            'product_category': '',
            'product_category_edited': '',
            'source': 'deliveroo.co.uk',
            'source_type': 'Website',
            'region': 'UK',
            'picture': row['image_background'],
        }
        df = pd.DataFrame(data, index=[0])
        self.to_stg_db(df)

    def to_stg_db(self, data_frame):
        DataBase().to_stg_table(data_frame=data_frame, name_stg_table='stg_promo')


class DominosPromoToPromoDB():
    def __init__(self):
        # self.address = {}
        self.city = {}
        # self.post_code = {}
        for df_address in next(self.get_address()):
            df_address.apply(lambda x: self.city.update({x['post_code_for_search']: x['city']}), axis=1)

        data = DataBase().get_table('stg_dominos_promo')
        for df in next(data):
            df.apply(self.convert, axis=1)

    def get_address(self):
        for df_html in DataBase().get_table('DIM_DOMINOS_INFO', chunksize=100):
            yield df_html

    def convert(self, row: pd.Series):
        data = {
            'start_date': row['date'],
            'end_date': row['date'],
            'brand': 'Dominos',
            'segment': '',
            'city': self.city[row['post_code']],
            'postcode': row['post_code'],
            'title': 'voucher' if row['voucher']=='Not found' else 'collect_deals',
            'promo_description_1_8': row['voucher'] if row['voucher']=='Not found' else row['collect_deals'],
            'promo_type': '',
            'promo_type_edited': '',
            'app_in_store': '',
            'promo_title_edited': '',
            'product_category': '',
            'product_category_edited': '',
            'source': 'https://www.dominos.co.uk/',
            'source_type': 'Website',
            'region': 'UK',
            'picture': row['image'],
        }
        df = pd.DataFrame(data, index=[0])
        self.to_stg_db(df)

    def to_stg_db(self, data_frame):
        DataBase().to_stg_table(data_frame=data_frame, name_stg_table='stg_promo')


class JustEatsPromoToPromoDB():
    def __init__(self):
        data = DataBase().get_table('stg_just_eats_promo')
        for df in next(data):
            df.apply(self.convert, axis=1)


    def convert(self, row: pd.Series):
        data = {
            'start_date': row['date'],
            'end_date': row['date'],
            'brand': 'Just eats',
            'segment': '',
            'city': row['city'],
            'postcode': row['post_code'],
            'title': row['head'],
            'promo_description_1_8': row['discounts'],
            'promo_type': '',
            'promo_type_edited': '',
            'app_in_store': '',
            'promo_title_edited': '',
            'product_category': '',
            'product_category_edited': '',
            'source': 'https://www.just-eat.co.uk/offers',
            'source_type': 'Website',
            'region': 'UK',
            'picture': row['promo_image'],
        }
        print(data)
        df = pd.DataFrame(data, index=[0])
        self.to_stg_db(df)

    def to_stg_db(self, data_frame):
        DataBase().to_stg_table(data_frame=data_frame, name_stg_table='stg_promo')


class BurgerKingPromoToPromoDB():
    def __init__(self):
        data = DataBase().get_table('stg_burger_king_promo')
        for df in next(data):
            df.apply(self.convert, axis=1)


    def convert(self, row: pd.Series):
        data = {
            'start_date': row['date'],
            'end_date': row['date'],
            'brand': 'Burger king',
            'segment': '',
            'city': row['city'],
            'postcode': row['post_code'],
            'title': row['head'],
            'promo_description_1_8': row['text'],
            'promo_type': '',
            'promo_type_edited': '',
            'app_in_store': '',
            'promo_title_edited': '',
            'product_category': '',
            'product_category_edited': '',
            'source': 'https://www.burgerking.co.uk/rewards/offers',
            'source_type': 'Website',
            'region': 'UK',
            'picture': row['image'],
        }
        print(data)
        df = pd.DataFrame(data, index=[0])
        self.to_stg_db(df)

    def to_stg_db(self, data_frame):
        DataBase().to_stg_table(data_frame=data_frame, name_stg_table='stg_promo')

class StarbucksPromoToPromoDB():
    def __init__(self):
        data = DataBase().get_table('stg_starbucks_promo')
        for df in next(data):
            df.apply(self.convert, axis=1)


    def convert(self, row: pd.Series):
        data = {
            'start_date': row['date'],
            'end_date': row['date'],
            'brand': 'Starbucks',
            'segment': '',
            'city': row['city'],
            'postcode': row['post_code'],
            'title': row['head'],
            'promo_description_1_8': row['text'],
            'promo_type': '',
            'promo_type_edited': '',
            'app_in_store': '',
            'promo_title_edited': '',
            'product_category': '',
            'product_category_edited': '',
            'source': 'https://www.starbucks.co.uk/rewards',
            'source_type': 'Website',
            'region': 'UK',
            'picture': '',
        }
        print(data)
        df = pd.DataFrame(data, index=[0])
        self.to_stg_db(df)

    def to_stg_db(self, data_frame):
        DataBase().to_stg_table(data_frame=data_frame, name_stg_table='stg_promo')

class McDonaldsPromoToPromoDB():
    def __init__(self):
        data = DataBase().get_table('stg_mcdonald_promo')
        for df in next(data):
            print(df)
            df.apply(self.convert, axis=1)


    def convert(self, row: pd.Series):
        data = {
            'start_date': row['date'],
            'end_date': row['date'],
            'brand': 'McDonalds',
            'segment': '',
            'city': 'London',
            'postcode': row['postcode'],
            'title': row['item'],
            'promo_description_1_8': row['description'],
            'promo_type': '',
            'promo_type_edited': '',
            'app_in_store': '',
            'promo_title_edited': '',
            'product_category': '',
            'product_category_edited': '',
            'source': row['source'],
            'source_type': 'Website',
            'region': 'UK',
            'picture': '',
        }
        print(data)
        df = pd.DataFrame(data, index=[0])
        self.to_stg_db(df)

    def to_stg_db(self, data_frame):
        DataBase().to_stg_table(data_frame=data_frame, name_stg_table='stg_promo')