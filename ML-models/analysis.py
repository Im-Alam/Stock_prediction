from bs4 import BeautifulSoup
import pandas as pd
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from keras import regularizers


class lstm:
    def __init__(self, df):
        self.df = df
        self.model = Sequential()

    def build_model():
        pass

    def model_data():
        pass
    
    def train(self):
        pass

    def predict(self, data_):
        pass
        
    


class xgb:
    pass




class sentimentAnalysis:
    def __init__(self,model_path):
        self.model = model_path
        self.df = pd.DataFrame(columns=['source_url','info','sentiment'])

    def scrapWeb1(self, url):
        pass

    def scrapWeb2(self, url):
        pass

    def scrapWeb3(self, url):
        pass

    def scrapWeb4(self, url):
        pass


    def collectInfo(self):
        pass
    
    def predictSentiment(self):
        sentiment = 'posetive'
        return sentiment

class chatBot:
    pass