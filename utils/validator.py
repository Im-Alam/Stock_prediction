import pandas as pd
from datetime import datetime 

#It checks for appropriate columns in dataset

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
