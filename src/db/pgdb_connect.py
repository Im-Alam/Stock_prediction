import os
from sqlalchemy import create_engine

def connectPGDB():
    try:
        engine = create_engine(os.getenv("AIVEN_PG_URI"))
        print("Lazy connection setup")
        return engine
    except Exception as e:
        print("Failed to connect database\n","-"*50,"\n",e)
        return 400

engine = connectPGDB()
