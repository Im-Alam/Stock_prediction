import pandas as pd
from datetime import datetime
from src.db_models.INDEX import IndicesTable
from src.utils.reqRes import apiError
import json

"""
1. get daily data of nifty index
2. Calculate correlation with indian market and foriegn market
3. Get data of foriegn exchange, make its min to zero by shifting and return the data for plot
"""


indian_index = ['nifty50','sensex','bank_nifty','nifty_auto', 'nifty_it','nifty_pharma']
foreign_index = ['dow_jones','nasdaq','s_and_p_500','ftse_100','dax','nikkei_225','shanghai_composite']
index_tickers = {
    'nifty50': '^NSEI',                  # NIFTY 50 (India)
    'sensex': '^BSESN',                  # SENSEX (India)
    'bank_nifty': '^NSEBANK',            # Bank Nifty (India)
    'nifty_auto': '^CNXAUTO',            # Nifty Auto (India)
    'nifty_it': '^CNXIT',                # Nifty IT (India)
    'nifty_pharma': '^CNXPHARMA',        # Nifty Pharma (India)
    'dow_jones': '^DJI',                 # Dow Jones (USA)
    'nasdaq': '^IXIC',                   # NASDAQ (USA)
    's_and_p_500': '^GSPC',              # S&P 500 (USA)
    'ftse_100': '^FTSE',                 # FTSE 100 (UK)
    'dax': '^GDAXI',                     # DAX (Germany)
    'nikkei_225': '^N225',               # Nikkei 225 (Japan)
    'shanghai_composite': '000001.SS'     # Shanghai Composite (China)
}


def predict(n_days:int = 5):
    pass

def display_prediction():
    pass

def update_prediction():
    pass



def calculate_corr():
    """
    data = [
        {'nifty50': 15000, 'sensex': 50000, 'bank_nifty': 32000, 'nifty_auto': 12000, 'nifty_it': 25000, 'nifty_pharma': 13000,
        'dow_jones': 34000, 'nasdaq': 14000, 's_and_p_500': 4200, 'ftse_100': 7000, 'dax': 15000, 'nikkei_225': 29000, 'shanghai_composite': 3500},
        {'nifty50': 15100, 'sensex': 50500, 'bank_nifty': 32200, 'nifty_auto': 12100, 'nifty_it': 25200, 'nifty_pharma': 13100,
        'dow_jones': 34500, 'nasdaq': 14500, 's_and_p_500': 4300, 'ftse_100': 7100, 'dax': 15200, 'nikkei_225': 29500, 'shanghai_composite': 3600},
        {'nifty50': 15200, 'sensex': 51000, 'bank_nifty': 32400, 'nifty_auto': 12200, 'nifty_it': 25400, 'nifty_pharma': 13200,
        'dow_jones': 35000, 'nasdaq': 15000, 's_and_p_500': 4400, 'ftse_100': 7200, 'dax': 15400, 'nikkei_225': 30000, 'shanghai_composite': 3700},    
    ]
    """
    try:
        data = IndicesTable.fetch_recent_nData(100)
    
        # Segregate data
        indian_data = []
        foreign_data = []

        for record in data:
            indian_entry = {}
            foreign_entry = {}
            
            for key, value in record.items():
                if key in indian_index:
                    indian_entry[key] = value
                elif key in foreign_index:
                    foreign_entry[key] = value
            
            indian_data.append(indian_entry)
            foreign_data.append(foreign_entry)

        #Convert to dataframe
        indian_df = pd.DataFrame(indian_data)
        foreign_df = pd.DataFrame(foreign_data)

        # Calculate the correlation matrix for Indian indices
        indian_corr_json = indian_df.corr().to_json(orient='index')

        # Calculate the correlation matrix for Foreign indices
        foreign_corr_json = foreign_df.corr().to_json(orient='index')

        return indian_corr_json, foreign_corr_json, json.dump(indian_data), json.dump(foreign_data)
    except Exception as e:
        return apiError(400, f'{e}')



