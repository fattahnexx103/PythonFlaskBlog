import pymongo

__author__ = 'neehad'

class Database(object): #Database inherits from object

    URI = "mongodb://127.0.0.1:27017" #mongod server address or instance
    DATABASE = None #no multiple use of the URI so only 1 uri for many database

    @staticmethod #we will not use self but rather get static variables for usage
    def initialize():
        client = pymongo.MongoClient(Database.URI)
        Database.DATABASE = client["SampleDatabase"]

    @staticmethod
    def insert(collection, data):
        Database.DATABASE[collection].insert(data)

    @staticmethod
    def find(collection, query):
        return Database.DATABASE[collection].find(query)

    @staticmethod
    def find_one(collection, query):
        return Database.DATABASE[collection].find_one(query)
