from django.shortcuts import render
from transactions.serializers import TransactionSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from utils import get_database
from bson.objectid import ObjectId
from bson import json_util
from bson.json_util import dumps
import json
from transactions.services.transfer_fund import FundTransfer


class TransactionList(APIView):
	'''List all transactions or create new transaction'''

	def get(self, request):
		db = get_database()
		transactions_collection = db['transactions']
		document = transactions_collection.find({})
		list_cur = list(document)
		return Response(json.loads(json_util.dumps(list_cur)))
	

	def post(self, request):
		db = get_database()
		serializer = TransactionSerializer(data=request.data)
		if serializer.is_valid():
			transactions_collection = db['transactions']
			transactions_collection.insert_one(serializer.data)
			sender_id = serializer.data['sender_id']
			receiver_id = serializer.data['receiver_id']
			amount = serializer.data['amount']
			# deduct from sender, add fund to receiver
			fund_transfer = FundTransfer(sender_id, receiver_id, amount)
			transfer_success = fund_transfer.transfer_fund_to_receiver(serializer.data)
			if transfer_success:
				return Response(transfer_success, status=status.HTTP_201_CREATED)
			else:
				return Response({'message': 'Fund could not be transferred.. please try again later'})
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	

class Transaction(APIView):
	'''get transaction details'''

	def get(self, request, transaction_id):
		db = get_database()
		transactions_collection = db['transactions']
		if transaction_id:
			document = transactions_collection.find({"_id": ObjectId(transaction_id)})
			list_cur = list(document)
			# Converting to the JSON
			if list_cur:
				return Response(json.loads(json_util.dumps(list_cur)))
			else:
				return Response({'message': 'No data found'})
		else:
			return Response({'message': 'Please enter transaction_id'})
