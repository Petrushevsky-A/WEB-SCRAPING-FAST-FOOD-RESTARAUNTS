
from sqlalchemy import MetaData, Table, Column, Integer, Text

MODELTABLE = Table(
                        'STG_HOTUKDEALS_BURGERKING_DEALS_CARDS', MetaData(),
                        Column('deals_card', Text())
                  )