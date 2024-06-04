from bs4 import BeautifulSoup
import pandas as pd

class lstm:
    def __init__(self, df):
        self.df = df

    def build_model():
        pass

    def model_data():
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