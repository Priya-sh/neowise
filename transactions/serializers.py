from rest_framework import serializers


class TransactionSerializer(serializers.Serializer):
	
	sender_id = serializers.CharField(required=True)
	receiver_id = serializers.CharField(required=True)
	amount = serializers.DecimalField(required=True, max_digits=6, decimal_places=2)
	details = serializers.CharField(required=False, max_length=255)