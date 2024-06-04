import pandas as pd
import numpy as np
from datetime import datetime

#from sklearn.preprocessing import StandardScaler

#from tensorflow.keras.models import Sequential
#from tensorflow.keras


def checkFormat(df_):
    df = df_.copy()
    #Converting column name to lowercase
    if df.shape[0]<100:
        return "TOO SHORT DATA"
    
    df.columns = [col.lower() for col in df.columns]
    required_columns = ['open', 'close', 'high', 'low']

    if not all(col in df.columns for col in required_columns):
        return "REQ COLUMNS"
    
    # Check if any 'date'-like column exists
    date_col = df.filter(like='date').columns[0]
    if df.filter(like='date').empty:
        return "DATE NOT FOUND"
    else:
        #print((date_col.iloc[1]-date_col.iloc[]))
        df[date_col] = [datetime.strptime(date_str, "%Y-%m-%d") for date_str in df[date_col]]
        return (min(df.loc[1,date_col]-df.loc[0,date_col], df.loc[2,date_col]-df.loc[1,date_col]))

    


class featureEngineering:
    def __init__(self) -> None:
          pass  
                         



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


    def CupAndHandle(self):
        pass

    def supportAndResistance(self):
        pass

    def bullBear(self):
        pass