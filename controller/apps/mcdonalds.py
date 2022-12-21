
from database.database import DataBase

from datetime import datetime

from multiprocessing import Pool
import pandas as pd
from functools import wraps

from parsers.apps.mcdonalds.mcdonalds import McDonaldsAppParser
class McDonaldsAppController():

    def __init__(self):
        # data_for_scraping = next(next(self.get_data_for_scraping())).iterrows()
        #
        # with Pool(processes=5) as pool:
        #     pool.map(self.scraping, data_for_scraping)
        self.scraping()
        pass
    # def get_data_for_scraping(self) -> pd.DataFrame:
    #     for df in DataBase().get_table('deliveroo_list_urls', chunksize=100):
    #         yield df

    def __start_scraping(function):
        @wraps(function)
        def wrapper(self, *arg):
            try:
                function(self)
            except Exception as ex:
                print(ex)

        return wrapper

    @__start_scraping
    def scraping(self):
        date = datetime.now().strftime("%d.%m.%Y")

        with McDonaldsAppParser() as parser:
            pass

    def to_stg_db(self, data_frame, name_stg_table):
        DataBase().to_stg_table(data_frame=data_frame, name_stg_table=name_stg_table)

