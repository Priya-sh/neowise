from django.shortcuts import render
from transactions.serializers import SnippetSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Create your views here.

class TransactionList(APIView):
	'''List all transactions or create new'''

	def get(self, request, format=None):
		pass
	

	def post(self, request, format=None):
		serializer = SnippetSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)