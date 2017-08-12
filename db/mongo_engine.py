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

    def add_entry(self, json):
        query = {}
        query['username'] = json['username']
        if self.collection.find(query).count() > 0:
            print('more then one document with that username')
            return False  # already have a document!
        self.collection.insert_one(json)
        return True  # implement exit statuses?

    def entry_exists(self, username):
        query = {}
        query['username'] = username
        if self.collection.find(query).count() > 0:
            return True
        else:
            return False

    def remove_by_username(self, username):
        query = {}
        query['username'] = username
        self.collection.delete_one(query)

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
            return cursor[0]  # finds 1st -> might lead to bugs later
        else:
            return {}  # empty dict == False
            # raise error? placeholder error object?


if __name__ == "__main__":
    pass
