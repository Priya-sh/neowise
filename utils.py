from pymongo import MongoClient


def get_database():
	# connect to mongo atlas cluster
	CONNECTION_STRING = "mongodb+srv://admin:Admin%402023@neowise.gi2pbcz.mongodb.net/?retryWrites=true&w=majority"

	client = MongoClient(CONNECTION_STRING)

	# create database named fund_transfer
	return client['fund_transfer']


if __name__ == '__main__':
	
	dbname = get_database()