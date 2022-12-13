# import pymysql
import psycopg2
import pandas as pd
from sqlalchemy import create_engine



from setting import DATABASES
# from .GetModel import TABLE

from datetime import datetime

class DataBase():

    def __init__(self):

        self.connect_db = self.connect()

    def connect(self):
        user = DATABASES['user']
        password = DATABASES['password']
        host = DATABASES['host']
        database = DATABASES['database']
        # 'postgresql+psycopg2://username:password@host:port/database'
        # return create_engine(f'mysql+pymysql://{user}:{password}@{host}/{database}')
        # return create_engine(rf'postgresql+psycopg2://{user}:{password}@{host}/{database}')
        return create_engine(rf'postgresql://{user}:{password}@{host}/{database}')


    def get_table(self, name_table, chunksize=100):
        name_table = name_table.lower()
        yield pd.read_sql_table(name_table, self.connect_db, chunksize=chunksize)


    # def get_table(self, name_table, params=None,name_column_date='', chunksize=100):
    #     if not params:
    #         params = [datetime.now().strftime("%d.%m.%Y"), 'date']
    #     else:
    #         params.extend(name_column_date)
    #
    #     query = f"SELECT * FROM {name_table} WHERE %s=%x"
    #     data = pd.read_sql(query, self.connect_db, chunksize=chunksize, params=params)
    #     yield data

    def to_stg_table(self, data_frame: pd.DataFrame, name_stg_table: str):
        name_stg_table = name_stg_table.lower()
        data_frame.to_sql(name_stg_table, self.connect_db, if_exists='append', index=False)
        return True
