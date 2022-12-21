import time

from database.database import DataBase

from datetime import datetime

from multiprocessing import Pool
import pandas as pd
from functools import wraps

from parsers.website.price.uber_eats.uber_eats import UberEatsPriceParser
class UberEatsPriceController():

    def __init__(self):
        data_for_scraping = next(next(self.get_data_for_scraping())).iterrows()

        for row in data_for_scraping:
            self.scraping(row)
        # with Pool(processes=1) as pool:
        #     pool.map(self.scraping, data_for_scraping)

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
                function(self, url, post_code_for_search, city)
            except ValueError as ex:
                print(ex)

        return wrapper

    @__start_scraping
    def scraping(self, url, post_code, city):
        date = datetime.now().strftime("%d.%m.%Y")

        with UberEatsPriceParser(url) as parser:

            time.sleep(3333)
            pass

    def to_stg_db(self, data_frame, name_stg_table):
        DataBase().to_stg_table(data_frame=data_frame, name_stg_table=name_stg_table)

