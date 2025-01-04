from rest_framework import serializers
from models.models_sqlalchemy import Message

from rest_framework import serializers

class MessageSerializer(serializers.Serializer):
    message_id = serializers.IntegerField(source='id')
    sender_id = serializers.IntegerField()
    recipient_id = serializers.IntegerField()
    content = serializers.CharField()
    response = serializers.CharField(allow_null=True)
    timestamp = serializers.DateTimeField()

    # Define any custom fields or transformations if needed