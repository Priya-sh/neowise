import json
from create_database import get_database

# create database and return the client object
print("Creating database and getting the client object")
dbname = get_database()

# create users collection
print("Creating users collection")
users_collection = dbname['users']

# insert json data into users collection
print("Inserting json into user collection")
with open('users.json') as f:
	user_data = json.load(f)
users_collection.insert_many(user_data)

# create a transactions collection
print("creating transactions collection")
transactions_collection = dbname['transactions']

print("Completed..")