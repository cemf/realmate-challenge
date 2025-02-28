from django.forms import ValidationError
from django.http import JsonResponse
from conversations.models import Conversation
from conversations.services import (
    add_message_to_conversation,
    close_conversation,
    create_open_conversation,
)


def handle_new_conversation(data):
    try:
        conversation = create_open_conversation(data["data"]["id"], data["timestamp"])
        return JsonResponse(
            {
                "status": "success",
                "message": "Conversation created successfully",
                "conversation_id": str(conversation.id),
                "timestamp": data["timestamp"],
            },
            status=201,
        )
    except Exception as e:
        error_message = str(e).strip("[]'")
        return JsonResponse({"status": "error", "message": error_message}, status=400)


def handle_new_message(data):
    try:
        message = add_message_to_conversation(
            data["data"]["id"],
            data["data"]["conversation_id"],
            data["data"]["content"],
            data["data"]["direction"],
        )
        return JsonResponse(
            {
                "status": "success",
                "message": "Message added successfully",
                "message_id": str(message.id),
                "conversation_id": str(message.conversation_id),
                "timestamp": data["timestamp"],
            },
            status=201,
        )
    except ValidationError as e:
        error_message = e.error_list[0].message
        return JsonResponse({"status": "error", "message": error_message}, status=400)
    except Conversation.DoesNotExist:
        return JsonResponse(
            {"status": "error", "message": "Conversation not found"}, status=404
        )
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=400)


def handle_close_conversation(data):
    try:
        conversation = close_conversation(data["data"]["id"], data["timestamp"])
        return JsonResponse(
            {
                "status": "success",
                "message": "Conversation closed successfully",
                "conversation_id": str(conversation.id),
                "timestamp": data["timestamp"],
            },
            status=200,
        )
    except Conversation.DoesNotExist:
        return JsonResponse(
            {"status": "error", "message": "Conversation not found"}, status=404
        )
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=400)
