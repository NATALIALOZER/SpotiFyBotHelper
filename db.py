import pymongo
 
client = pymongo.MongoClient('mongodb://localhost/tutorial_bot3')
users_db = client.get_database()["users_db"]