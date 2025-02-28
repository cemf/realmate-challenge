import json
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Conversation, Message
import uuid

ID_CHAT = str(uuid.uuid4())
ID_MESSAGE1 = str(uuid.uuid4())
ID_MESSAGE2 = str(uuid.uuid4())

class ConversationDetailTestCase(APITestCase):
    def setUp(self):
        # Cria uma conversa e mensagens para teste

        self.conversation = Conversation.objects.create(
            id=ID_CHAT, status=Conversation.STATUS_OPEN
        )

        self.message1 = Message.objects.create(
            id=ID_MESSAGE1,
            conversation_id=ID_CHAT,
            text="Olá, tudo bem?",
            direction=Message.TYPE_SENT,
        )
        self.message2 = Message.objects.create(
            id=ID_MESSAGE2,
            conversation_id=ID_CHAT,
            text="Tudo bem, e você?",
            direction=Message.TYPE_RECEIVED,
        )

    def test_get_conversation_detail(self):
        url = reverse("conversation-detail", args=[self.conversation.id])

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        expected_data = {
            "id": ID_CHAT,
            "status": "OPEN",
            "messages": [
                {
                    "id": ID_MESSAGE1,
                    "text": "Olá, tudo bem?",
                    "direction": "SENT",
                    "created_at": self.message1.created_at.strftime(
                        "%Y-%m-%dT%H:%M:%S.%fZ"
                    ),
                },
                {
                    "id": ID_MESSAGE2,
                    "text": "Tudo bem, e você?",
                    "direction": "RECEIVED",
                    "created_at": self.message2.created_at.strftime(
                        "%Y-%m-%dT%H:%M:%S.%fZ"
                    ),
                },
            ],
        }
        self.assertEqual(response.json()["id"], expected_data["id"])
        self.assertEqual(response.json()["status"], expected_data["status"])
        self.assertEqual(
            response.json()["messages"][0]["id"], expected_data["messages"][0]["id"]
        )
        self.assertEqual(
            response.json()["messages"][0]["direction"],
            expected_data["messages"][0]["direction"],
        )
        self.assertEqual(
            response.json()["messages"][0]["created_at"],
            expected_data["messages"][0]["created_at"],
        )
        self.assertEqual(
            response.json()["messages"][1]["id"], expected_data["messages"][1]["id"]
        )
        self.assertEqual(
            response.json()["messages"][1]["direction"],
            expected_data["messages"][1]["direction"],
        )
        self.assertEqual(
            response.json()["messages"][1]["created_at"],
            expected_data["messages"][1]["created_at"],
        )

    def test_get_conversation_detail_not_found(self):

        url = reverse(
            "conversation-detail", args=["00000000-0000-0000-0000-000000000000"]
        )
        
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        self.assertEqual(
            response.json(), {"status": "error", "message": "Conversation not found"}
        )

