import pymysql
import pandas as pd
from sqlalchemy import create_engine

from setting import DATABASES




class DataBase():

    def __init__(self):
        # self.connect_db = pymysql.connect(
        #                                     **DATABASES,
        #                                     cursorclass = pymysql.cursors.DictCursor,
        #                                  )

        user = DATABASES['user']
        password = DATABASES['password']
        host = DATABASES['host']
        database = DATABASES['database']
        self.connect_db = create_engine(f'mysql+pymysql://{user}:{password}@{host}/{database}')  # fill details

    def connect(self):
         pass

    def get_urls(self):
        with self.connect_db, self.connect_db.cursor() as cursor:
            cursor.execute('select * from test;')
            return cursor.fetchmany()


    def create_stg_table(self, data_frame: pd.DataFrame, name_stg_table: str):
        data_frame.to_sql(name_stg_table, self.connect_db, if_exists='append', index=False)
