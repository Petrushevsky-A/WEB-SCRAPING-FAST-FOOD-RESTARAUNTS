
from parsers.website.promo.gmail.gmail import GmailParsePromo

import pandas as pd
import time
from datetime import datetime
import itertools

from database.database import DataBase

class GmailPromoController():

    def __init__(self):
        self.scraping()

    def scraping(self):
        with GmailParsePromo() as parser:

            count_message = parser.get_count_messages()
            print(count_message)

            city = "London"
            post_code = "W1C 1LX"
            date = datetime.now().strftime("%d.%m.%Y")


            for number_message in range(1, count_message+1):
                parser.open_message(number_message)

                head = parser.get_head()
                print(f'head {head}')
                image = parser.get_image()
                print(f'image {image}')
                description = parser.get_description()
                print(f'description {description}')
                hash_id = parser.get_hash_id()
                print(f'hash_id {hash_id}')

                html_message = parser.get_html_message()
                print('='*33)
                print(html_message)
                print('='*33)


                data= {
                    'date':date,
                    'post_code':post_code,
                    'city':city,
                    'head':head,
                    'image':image,
                    'text':description,
                    'hash_id':hash_id,
                    'html_message':html_message,
                }


                data_frame = pd.DataFrame(data, index=[0])
                self.to_stg_db(data_frame, 'STG_GMAIL_CARDS')

                parser.navigate_back()


    def to_stg_db(self, data_frame, name_stg_table):
        DataBase().to_stg_table(data_frame=data_frame, name_stg_table=name_stg_table)
