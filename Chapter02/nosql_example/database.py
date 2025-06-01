from pymongo import MongoClient

client = MongoClient()
# equivalent to
# client = MongoClient("mongodb://localhost:27017")


database = client.fastapimongodb
user_collection = database["users"]
