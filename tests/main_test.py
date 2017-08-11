#!/usr/bin/env python3
from db import mongo_engine
from db import json_engine as je


def testf():
    tj = je.newSimpleJS(name='Johanna', username='@User',city='Moscow', bio='hello world!')
    db = mongo_engine.mongo()
    db.add_entry(tj)
    db.find_by_username('@User')


def main():
    testf()


if __name__ == "__main__":
    main()
