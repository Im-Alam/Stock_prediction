import pandas as pd
import numpy as np
from datetime import datetime

#from sklearn.preprocessing import StandardScaler

#from tensorflow.keras.models import Sequential
#from tensorflow.keras


def checkFormat(df):
    #Return Type: {"REQ COL":"Doesn't contain required columns", "DAT NF": Date not found}
    
    #Converting column name to lowercase
    df.columns = [col.lower() for col in df.columns]
    required_columns = ['open', 'close', 'high', 'low']

    if not all(col in df.columns for col in required_columns):
        return "REQ COL"
    
    # Check if any 'date'-like column exists
    date_col = df.filter(like='date')
    if df.filter(like='date').empty:
        return "DAT NF"
    else:
        return df[date_col[0]][1]-df[date_col[0]][0]

    




class FindPattern:
    def __init__(self, data_):
        # data is a dataframe
        self.data_ = data_


    def hammerAndHang_man(self):
        table = self.data_.copy()
        table.columns = [col.lower() for col in table.columns]
        np_table = np.array(table[['open', 'close', 'high', 'low']])

        hammer_indices = []
        for row in np_table:
            open_price, close_price, high_price, low_price = row

            # Check conditions for inverted hammer
            body_size = abs(open_price - close_price)
            upper_wick_size = high_price - max(open_price, close_price)
            lower_wick_size = min(open_price, close_price) - low_price

            if (body_size < (high_price - low_price) / 4):
                    if upper_wick_size > 3 * body_size:
                        hammer_indices.append(1)
                    if lower_wick_size > 3 * body_size:
                        hammer_indices.append(-1)
            else:
                hammer_indices.append(0)
                
        return hammer_indices
