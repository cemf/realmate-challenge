from rest_framework import serializers
from .models import Message
from .models import Conversation


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'text', 'direction', 'created_at']
        
class ConversationSerializer(serializers.ModelSerializer):
    messages = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['id', 'status', 'messages','start_conversation_date','end_conversation_date']
    
    def get_messages(self, obj):
        
        messages = Message.objects.filter(conversation_id=obj.id)
        return MessageSerializer(messages, many=True).data