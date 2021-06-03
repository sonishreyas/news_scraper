from pymongo import MongoClient
import datetime
from os import environ
from dotenv import load_dotenv

class MongoDB():
    def __init__(self):
        load_dotenv('/home/ubuntu/BE/news_scraper/src/configs/.env.prod')
        self.client = MongoClient(f"mongodb://{environ.get('MONGO_USER')}:{environ.get('MONGO_PWD')}@{environ.get('MONGO_IP')}:{environ.get('MONGO_PORT')}/{environ.get('MONGO_DATABASE')}",authSource=environ.get("MONGO_DATABASE_AUTHENTICATION")) 
        self.mydb = self.client[environ.get("MONGO_DATABASE")]
        
    def insert(self, collection_name, data):
        collection = getattr(self.mydb, collection_name)
        object_id = collection.insert(data)
        return object_id

    def insert_many(self, collection_name, data):
        print("insert karlo")
        collection = getattr(self.mydb, collection_name)
        object_id = collection.insert_many(data)
        return object_id
    
    def find_and_update(self, collection_name, new_fields, search={}):
        collection = getattr(self.mydb, collection_name)
        collection.update_one(
            search, 
            {"$set": new_fields}
        )

    def find_entries(self, collection_name, search={}, keys_to_extract=['_id']):
        collection = getattr(self.mydb, collection_name)
        cq = []
        for post in collection.find(search):
            cq.append({key: post[key] for key in keys_to_extract})
        return cq

    def close_connection(self):
        self.client.close()


