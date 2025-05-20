from rest_framework import serializers

class ContactSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=75)
    email = serializers.EmailField(max_length=100)
    message = serializers.CharField(max_length=1000)
