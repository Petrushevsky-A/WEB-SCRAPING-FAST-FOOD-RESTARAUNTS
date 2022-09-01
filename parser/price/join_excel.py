from datetime import datetime

import pandas as pd
import os
# brand = 'dominos_banner'
# brand = 'dominos'
# brand = 'dominos_collect_deals'
# brand = 'dominos_vouchers'
# brand = 'just_eats'
# brand = 'result_menu_price'
# brand = 'uber_eats'
# brand = 'deliveroo'
file_name = [i for i
             in os.listdir(r'.') if (brand in i) and ('xlsx' in i) and not ('list' in i)]


print(len(file_name))


temp = []

for i in file_name:
  temp.append(pd.read_excel(f'{i}', index_col=[0]))
date = datetime.now().strftime("%d.%m.%Y")
pd.concat(temp).to_excel(f"{brand}_{str(date)}.xlsx")

