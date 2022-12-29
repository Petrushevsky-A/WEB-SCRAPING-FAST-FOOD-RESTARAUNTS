import time

from database.database import DataBase

from datetime import datetime

from multiprocessing import Pool
import pandas as pd
from functools import wraps

from parsers.website.price.uber_eats.uber_eats import UberEatsPriceParser


from itertools import product
class UberEatsPriceController():

    def __init__(self):
        data_for_scraping = next(next(self.get_data_for_scraping())).iterrows()

        with Pool(processes=1) as pool:
            pool.map(self.scraping, data_for_scraping)

    def get_data_for_scraping(self) -> pd.DataFrame:
        for df in DataBase().get_table('uber_eats_list_url', chunksize=100):
            yield df

    def __start_scraping(function):
        @wraps(function)
        def wrapper(self, data):
            try:
                _, row = data
                url = row['url']
                post_code_for_search = row['post_code']
                city = row['city']
                print(url, post_code_for_search, city)
                function(self, url, post_code_for_search, city)
            except ValueError as ex:
                print(ex)


        return wrapper

    @__start_scraping
    def scraping(self, url, post_code_for_search, city):
            date = datetime.now().strftime("%d.%m.%Y")
            with UberEatsPriceParser(url) as parser:

                address = parser.get_address()
                print(f'address {address}')
                post_code = parser.get_post_code(address)
                print(f'post_code {post_code}')
                count_cards = parser.get_count_items()
                print(f'len cards {count_cards}')
                head = parser.get_head()
                print(f'brand {head}')
                brand = parser.get_brand()
                print(f'brand {brand}')

                for id_card in range(1, count_cards+1):
                    parser.base_price = 0
                    parser.sizes = []
                    parser.prices = []
                    print(f'id_card {id_card}')
                    parser.scrolling_to_card(id_card)

                    category = parser.get_category(id_card)
                    print(category)


                    parser.open_item_card(id_card)

                    title_item = parser.get_title_item()
                    print(f'title_item {title_item}')

                    description = parser.get_description()
                    print(f'description {description}')
                    image_url = parser.get_image_url()
                    print(f'image_url {image_url}')
                    html_card = parser.get_html_card()
                    print(f'html_card {html_card}')
                    calories = parser.get_calories()
                    print(f'calories {calories}')


                    parser.get_base_price()
                    parser.size()
                    print(f'base price     ===============================================  {parser.base_price}')
                    print(f'price          ===============================================  {parser.prices}')
                    print(f'name size      ===============================================  {parser.sizes}')


                    parser.navigate_back()

                    # time.sleep(3333)
                    # continue
                    for price, size in zip(parser.prices, parser.sizes):
                        data = {
                                        'start_date': date,
                                        'end_date': '',
                                        'brand': brand,
                                        'address': address,
                                        'city': city,
                                        'post_code': post_code,
                                        'segment': '',
                                        'category': category,
                                        'category_2': size,
                                        'category_3': '',
                                        'category_4': '',
                                        'item': title_item,
                                        'source': 'https://deliveroo.co.uk',
                                        'region': 'UK',
                                        'price': price,
                                        'status': 'on',
                                        'picture': image_url,
                                        'html_cards': html_card,
                                        'post_code_address': post_code_for_search,
                                        'description': description,
                                        'calories': calories,
                                        'head':head,
                                        'url': url,
                                    }

                        data_frame = pd.DataFrame(data, index=[0])

                        self.to_stg_db(data_frame, 'STG_UBER_EATS_HTML_CARDS_NEW_SCRIPT_TEST')




                print('final')
                time.sleep(2222)


    def to_stg_db(self, data_frame, name_stg_table):
        DataBase().to_stg_table(data_frame=data_frame, name_stg_table=name_stg_table)

