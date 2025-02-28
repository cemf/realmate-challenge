from rest_framework.test import APITestCase
from rest_framework import status
import json
import unittest
from django.urls import reverse
from conversations.services import get_conversation_by_id
from webhook.views import EVENTS


class WebhookTestCase(APITestCase):
    def test_webhook_new_conversation(self):
        # URL do endpoint
        url = reverse("webhook")

        # Payload do webhook
        payload = {
            "type": "NEW_CONVERSATION",
            "timestamp": "2025-02-21T10:20:41.349308",
            "data": {"id": "6a41b347-8d80-4ce9-84ba-7af66f369f6a"},
        }

        response = self.client.post(
            url,
            data=json.dumps(payload),  # Converte o payload para JSON
            content_type="application/json",  # Define o tipo de conteúdo como JSON
        )
        conversation = get_conversation_by_id(payload["data"]["id"])

        # Verifica se a conversa foi criada
        self.assertIsNotNone(conversation)
        # Verifica se a conversa está com o status OPEN
        self.assertEqual(conversation.id, payload["data"]["id"])
        # Verifica se a conversa está com o status OPEN
        self.assertEqual(conversation.status, "OPEN")
        # Verifica se a conversa foi criada com a data correta
        self.assertEqual(
            conversation.start_conversation_date.replace(tzinfo=None).isoformat(),
            payload["timestamp"],
        )
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_data["status"], "success")

    def test_webhook_new_message_no_conversation(self):
        # URL do endpoint
        url = reverse("webhook")

        # Payload do webhook
        payload = {
            "type": "NEW_MESSAGE",
            "timestamp": "2025-02-21T10:20:44.349308",
            "data": {
                "id": "16b63b04-60de-4257-b1a1-20a5154abc6d",
                "direction": "SENT",
                "content": "Tudo ótimo e você?",
                "conversation_id": "6a41b347-8d80-4ce9-84ba-7af66f369f6a",
            },
        }

        response = self.client.post(
            url,
            data=json.dumps(payload),  # Converte o payload para JSON
            content_type="application/json",  # Define o tipo de conteúdo como JSON
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()["message"], "Conversation does not exist.")

    def test_webhook_new_message(self):
        # URL do endpoint
        url = reverse("webhook")

        conversation_id = "6a41b347-8d80-4ce9-84ba-7af66f369f6a"
        payload = {
            "type": "NEW_CONVERSATION",
            "timestamp": "2025-02-21T10:20:41.349308",
            "data": {"id": conversation_id},
        }

        response = self.client.post(
            url,
            data=json.dumps(payload),  # Converte o payload para JSON
            content_type="application/json",  # Define o tipo de conteúdo como JSON
        )
        conversation = get_conversation_by_id(payload["data"]["id"])

        # Verifica se a conversa foi criada
        self.assertIsNotNone(conversation)

        # Payload do webhook
        payload = {
            "type": "NEW_MESSAGE",
            "timestamp": "2025-02-21T10:20:44.349308",
            "data": {
                "id": "16b63b04-60de-4257-b1a1-20a5154abc6d",
                "direction": "SENT",
                "content": "Tudo ótimo e você?",
                "conversation_id": conversation_id,
            },
        }

        response = self.client.post(
            url,
            data=json.dumps(payload),  # Converte o payload para JSON
            content_type="application/json",  # Define o tipo de conteúdo como JSON
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()["status"], "success")

    def test_webhook_close_conversation(self):
        # URL do endpoint
        url = reverse("webhook")

        conversation_id = "6a41b347-8d80-4ce9-84ba-7af66f369f6a"
        payload = {
            "type": EVENTS["NEW_CONVERSATION"],
            "timestamp": "2025-02-21T10:20:45.349308",
            "data": {"id": conversation_id},
        }

        response = self.client.post(
            url,
            data=json.dumps(payload),  # Converte o payload para JSON
            content_type="application/json",  # Define o tipo de conteúdo como JSON
        )
        conversation = get_conversation_by_id(payload["data"]["id"])

        # Verifica se a conversa foi criada
        self.assertIsNotNone(conversation)

        # Payload do webhook
        payload = {
            "type": EVENTS["CLOSE_CONVERSATION"],
            "timestamp": "2025-02-21T10:20:44.349308",
            "data": {
                "id": "16b63b04-60de-4257-b1a1-20a5154abc6d",
                "conversation_id": conversation_id,
            },
        }

        response = self.client.post(
            url,
            data=json.dumps(payload),  # Converte o payload para JSON
            content_type="application/json",  # Define o tipo de conteúdo como JSON
        )
        conversation = get_conversation_by_id(conversation_id)
        # Verifica se a conversa foi fechada
        self.assertEqual(conversation.status, "CLOSED")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["status"], "success")


if __name__ == "__main__":
    unittest.main()
# Create your tests here.
