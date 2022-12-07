import pandas as pd

from database.database import DataBase

table_names = {
    'stg_nandos_price',
    'stg_deliveroo_price',
    'stg_just_eats_price',
    'stg_uber_eats_price',
}

class NandosPriceToPriceDB():
    def __init__(self):

        data = DataBase().get_table('stg_nandos_price')
        for df in next(data):
            self.to_stg_db(df)


    def to_stg_db(self, data_frame):
        DataBase().to_stg_table(data_frame=data_frame, name_stg_table='stg_price')

class DeliverooPriceToPiceDB():

    def __init__(self):
        data = DataBase().get_table('stg_deliveroo_price')
        for df in next(data):
            self.to_stg_db(df.rename(columns={"Price": "Price(£)"}))

    def to_stg_db(self, data_frame):
        DataBase().to_stg_table(data_frame=data_frame, name_stg_table='stg_price')

class JustEatsPriceToPiceDB():

    def __init__(self):
        data = DataBase().get_table('stg_just_eats_price')
        for df in next(data):
            self.to_stg_db(df.rename(columns={"Price": "Price(£)"}))

    def to_stg_db(self, data_frame):
        DataBase().to_stg_table(data_frame=data_frame, name_stg_table='stg_price')

class UberEatsPriceToPiceDB():

    def __init__(self):
        data = DataBase().get_table('stg_uber_eats_price')
        for df in next(data):
            self.to_stg_db(df.rename(columns={"Price": "Price(£)"}))

    def to_stg_db(self, data_frame):
        DataBase().to_stg_table(data_frame=data_frame, name_stg_table='stg_price')

