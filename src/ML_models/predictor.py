import random

def predict_next_n_day_price(n:int=5):
    return [1000 + 500*random.random() for _ in range(n)]