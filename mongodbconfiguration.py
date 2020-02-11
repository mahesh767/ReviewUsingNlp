from flask import  Flask
import pymongo
from start import  app
connectionstring="mongodb+srv://darwin:darwin@cluster0-ismdm.mongodb.net/test?retryWrites=true&w=majority"

client=pymongo.MongoClient(connectionstring)
database=pymongo.database.Database(client,'Customers')
collection=pymongo.collection.Collection(database,'Customer')

