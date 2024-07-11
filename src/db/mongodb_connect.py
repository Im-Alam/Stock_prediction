import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


#In mongoDB we dont require to close connection like sql. sql can crases if not closed after use.
def connectMDB():
    #specifying version of server api
    Server_api = ServerApi('1')
    # Create a new client and connect to the server
    try:
        client = MongoClient(os.getenv('MONGODB_URI'), server_api = Server_api)
    except Exception as e:
        return e
    
    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
        return client
    except Exception as e:
        return e
