import re

import pandas as pd
from lxml import html, etree
from database.database import DataBase
from datetime import datetime

class DominosCleaner():

    def __init__(self):
        self.address = {}
        self.city = {}
        self.post_code_for_search = {}
        for df_address in next(self.get_address()):
            df_address = df_address.set_index('post_code_for_search')
            self.address.update(df_address.to_dict()['address'])
            self.city.update(df_address.to_dict()['city'])
            self.post_code_for_search.update(df_address.to_dict()['post_code'])
            # self.post_code_for_search.update(df_address.to_dict()['post_code_for_search'])
            # print(self.post_code_for_search)
            # print(df_address)


        self.data = next(self.get_html())
        for df in self.data:
            self.clean(df)

    def get_html(self) -> pd.DataFrame:
        for df_html in DataBase().get_table('stg_dominos_html_cards', chunksize=100):
            yield df_html

    def get_address(self) -> pd.DataFrame:
        for df_html in DataBase().get_table('dim_dominos_info', chunksize=100):
            yield df_html

    def find(self, html_element, xpath, attribute = None, method = None, method_arguments = None, attribute_index = None, tostring = None):
        try:
            tree = html.fromstring(html_element)
            elements = tree.xpath(xpath)

            pattern = [k for k, v  in locals().items() if not v==None]
            match pattern:
                case [*t, 'attribute', 'attribute_index']:
                    return [i.__getattribute__(attribute)[attribute_index] for i in elements]
                case [*t, 'attribute', ]:
                    return [i.__getattribute__(attribute) for i in elements]
                case [*t, 'method', 'method_arguments']:
                    return [i.__getattribute__(method)(method_arguments) for i in elements]
                case [*t, 'method', ]:
                    return [i.__getattribute__(method)() for i in elements]

            if tostring:
                # return [i.text for i in elements]
                return [etree.tostring(i).decode("utf-8") for i in elements]


        except Exception as ex:
            return ['Not found', ]

    def parse(self, row: pd.Series):
        try:
            html_card = row['html_card']
            date_parse = row['date_parse']
            post_code = row['post_code']
            index_card = row['index_card']
            type_card = row['type_card']
            category = row['category']
            image = row['image']
            price = row['price']
            name = row['name']
            select = row['select']


            start_date = end_date = datetime.now().strftime("%d.%m.%Y")
            brand = 'Dominos'
            region = 'UK'
            status = 'on'
            source = 'https://www.dominos.co.uk/'
            address = self.address[post_code]

            city = self.city[post_code]
            post_code_address = self.post_code_for_search[post_code]


            try:
                category_two = select.split('£')[0]
            except:
                category_two = 'Not found'
            try:
                item = ''
                items = name.split('\n')
                for i in items:
                    if i:
                        item = i.strip()
                        break
                # item = next(iter(items))
            except:
                item = 'Not found'



            try:
                price = select.split('£')[1]
            except:
                price = 'Not found'
                try:
                    prices = re.findall(r'£(\d*\.\d*)', html_card)
                    price = next(iter(prices))
                except:
                    price = 'Not found'


            try:
                image = self.find(html_card, '//source ', attribute='attrib', attribute_index='srcset')
                picture = next(iter(image))
            except:
                picture = 'Not found'
            data = {
                        'start_date': start_date,
                        'end_date': end_date,
                        'brand': brand,
                        'address': address,
                        'city': city,
                        'post_code': post_code,
                        'segment': '',
                        'category': category,
                        'category_2': category_two,
                        'category_3': '',
                        'category_4': '',
                        'item': item,
                        'source': source,
                        'region': region,
                        'price': price,
                        'status': status,
                        'picture': picture,
                        'html_cards': html_card,
                        'post_code_address': post_code_address,
                        'select': select,
                    }
            print(data)
            self.to_stg_db(pd.DataFrame(data=data, index=[0]), 'DIM_DOMINOS_CLEAN_DATE')
        except ValueError as ex:
            print(ex)


    def to_stg_db(self, data_frame, name_stg_table):
        DataBase().to_stg_table(data_frame= data_frame, name_stg_table=name_stg_table)


    def clean(self, df):
        df.apply(self.parse, axis=1)