from pymongo import MongoClient 
from pprint import pprint
import os 


class Mongo:

    def __init__(self, mongo_uri, collection):

        self.mongo_uri = mongo_uri 
        self.client = MongoClient(self.mongo_uri)
        self.collection = collection
        self.db = self.client[collection]


    def insert_doc(self, result:dict) -> str:
        
        signal = self.db.results.insert_one(result)
        pprint(signal.inserted_id)

    def find_doc(self, query: dict) -> list:

        return self.db.results.find(query)
