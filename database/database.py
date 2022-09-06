import pymysql
import pandas as pd
from sqlalchemy import create_engine



from setting import DATABASES
# from .GetModel import TABLE


class DataBase():

    def __init__(self):

        self.connect_db = self.connect()

    def connect(self):
        user = DATABASES['user']
        password = DATABASES['password']
        host = DATABASES['host']
        database = DATABASES['database']
        return create_engine(f'mysql+pymysql://{user}:{password}@{host}/{database}')

    # def get_table(self, name_table):
    #     users_table = TABLE[name_table]
    #     result = self.connect_db.execute(users_table.select())
    #     return result.mappings().all()

    def get_table(self, name_table):
        return pd.read_sql_table(name_table, self.connect_db)


    def create_stg_table(self, data_frame: pd.DataFrame, name_stg_table: str):
        data_frame.to_sql(name_stg_table, self.connect_db, if_exists='append', index=False)

