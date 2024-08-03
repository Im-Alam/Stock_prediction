import pandas as pd
from datetime import datetime
from src.db_models.INDEX import IndexSchema


def predict_next_close():
    input_data = IndexSchema.getScrip(30)
    return model.fit(input_data)