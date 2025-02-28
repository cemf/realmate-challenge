from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from webhook.enums import EventType
from webhook.handlers import (
    handle_close_conversation,
    handle_new_conversation,
    handle_new_message,
)
from webhook.serializers import WebhookSerializer

@csrf_exempt
def webhook(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            serializer = WebhookSerializer(data=data)
            if not serializer.is_valid():
                return JsonResponse(
                    {"status": "error", "message": serializer.errors}, status=400
                )
            if data["type"] == EventType.NEW_CONVERSATION.value:
                return handle_new_conversation(data)
            elif data["type"] == EventType.NEW_MESSAGE.value:
                return handle_new_message(data)
            elif data["type"] == EventType.CLOSE_CONVERSATION.value:
                return handle_close_conversation(data)
            else:
                return JsonResponse(
                    {
                        "status": "error",
                        "message": "Invalid type. Expected 'NEW_CONVERSATION' or 'NEW_MESSAGE'",
                    },
                    status=400,
                )
        except json.JSONDecodeError:
            return JsonResponse(
                {"status": "error", "message": "Invalid JSON"}, status=400
            )
    else:
        return JsonResponse(
            {"status": "error", "message": "Method not allowed"}, status=405
        )


# Create your views here.
