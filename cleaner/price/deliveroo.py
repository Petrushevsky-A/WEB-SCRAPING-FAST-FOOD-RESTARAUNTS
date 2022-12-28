
import pandas as pd

class DeliverooPriceCleaner():
    def __init__(self, data_frame):
        data_frame = data_frame.apply(self.clean_row, axis=1)

    def clean_row(self, row: pd.Series):

        row['Item'] = row['Item'].replace(' &amp;', '')
        for e in row:
            if e in ('™', '®'):
                return row['Item'].replace(e, '')

        return row