
from sqlalchemy import MetaData, Table, Column, Integer, Text

MODELTABLE = Table(
                        'STG_DOMINOS_PRICE', MetaData(),
                        Column('deals_card', Text())
                  )