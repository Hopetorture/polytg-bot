#!/usr/bin/env python3
# import json

# make overloading method, turn into a class
def newSimpleJS(name = 'nullname', username = '@usernameTest', city = 'DC', bio = 'empty bio'):
    data = {}
    data['name'] = name
    data['username'] = username
    data['city'] = city
    data['bio'] = bio
    return data

if __name__ == "__main__":
    newSimpleJS()