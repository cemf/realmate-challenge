from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer

class ConversationDetailView(APIView):
    def get(self, id):
        try:
            conversation = Conversation.objects.get(id=id)
            serializer = ConversationSerializer(conversation)
            messages = Message.objects.filter(conversation_id=id)
            messages_serializer = MessageSerializer(messages, many=True)
            
            serializer.data["messages"] = messages_serializer.data
            
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Conversation.DoesNotExist:
            return Response(
                {"status": "error", "message": "Conversation not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
