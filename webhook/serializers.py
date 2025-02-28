from rest_framework import serializers

class WebhookSerializer(serializers.Serializer):
    type = serializers.CharField()
    timestamp = serializers.DateTimeField()
    data = serializers.DictField()