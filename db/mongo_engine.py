#!/usr/bin/env python3
from pymongo import MongoClient

class mongo:

    def __init__(self, database = 'telegram', collection = 'polyamorals'):
        self.client = MongoClient()
        self.db = self.client[database]
        self.collection = self.db[collection]

    def test(self, json_data):
        client = MongoClient()
        pdb = client.telegram
        collection = pdb.polyamorals
        collection.insert_one(json_data)

        print(42)


    def add_entry(self, json, database ='telegram', collection ='polyamorals'):
        client = MongoClient()
        pdb = client[database]
        collection = pdb[collection]
        query = {}
        query['username'] = json['username']
        if self.collection.find(query).count() > 0:
            print('more then one document with that username')
            return -1 # already have a document!
        collection.insert_one(json)
        return 0 #  implement exit statuses?

    def remove_by_username(self, username):
        # self.collection.
        pass

    def replace_by_username(self, username, json):
        query = {}
        query['username'] = username
        self.collection.replace_one(query, json)
        # NOT TESTED.
        

    def find_by_username(self, username):
        query = {}
        query['username'] = username
        cursor = self.collection.find(query)
        if cursor.count() > 0:
            print(cursor[0])
        else:
            return -1 # raise error?

        





if __name__ == "__main__":
    pass
