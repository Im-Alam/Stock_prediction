import os
from sqlalchemy import create_engine

trail_uri = 'SQL_LITE_URI'
deployment_uri = 'AIVEN_PG_URI'

def connectPGDB(uri=trail_uri):
    try:
        engine = create_engine(os.getenv(uri))
        print("Lazy connection setup")
        return engine
    except Exception as e:
        print("Failed to connect database\n","-"*50,"\n",e)
        return 400

engine = connectPGDB()
