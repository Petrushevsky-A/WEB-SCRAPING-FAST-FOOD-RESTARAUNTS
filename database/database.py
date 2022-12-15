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


    # def get_table(self, name_table, chunksize=100):
    #     name_table = name_table.lower()
    #     yield pd.read_sql_table(name_table, self.connect_db, chunksize=chunksize)


    def get_table(self, name_table, chunksize=100, date_param=None):
        '''
        :param name_table str :
        :param int : size DataFrame
        :param date List[str, str]: ['column_name_date', '17.08.2022']
        :yield DataFrame:
        '''
        name_table = name_table.lower()

        if date_param:
            query = f"SELECT * FROM {name_table} WHERE %s=%x"
            data = pd.read_sql(query, self.connect_db, chunksize=chunksize, params=date_param)
            yield data
        else:
            name_table = name_table.lower()
            yield pd.read_sql_table(name_table, self.connect_db, chunksize=chunksize)

    def to_stg_table(self, data_frame: pd.DataFrame, name_stg_table: str):
        name_stg_table = name_stg_table.lower()
        data_frame.to_sql(name_stg_table, self.connect_db, if_exists='append', index=False)
        return True
