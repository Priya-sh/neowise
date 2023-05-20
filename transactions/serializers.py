from rest_framework import serializers


class TransactionSerializer(serializers.Serializer):
	
	id = serializers.IntegerField(read_only=True)
	title = serializers.CharField(required=False, allow_blank=True, max_length=100)
	code = serializers.CharField(style={'base_template': 'textarea.html'})
	linenos = serializers.BooleanField(required=False)