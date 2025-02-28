from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from django.core.exceptions import ValidationError
from conversations.models import Conversation
from conversations.services import (
    add_message_to_conversation,
    close_conversation,
    create_open_conversation,
)

EVENTS = {
    "NEW_CONVERSATION": "NEW_CONVERSATION",
    "NEW_MESSAGE": "NEW_MESSAGE",
    "CLOSE_CONVERSATION": "CLOSE_CONVERSATION",
}


@csrf_exempt
def webhook(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            # Verifica se os campos obrigatórios estão presentes
            if all(key in data for key in ["type", "timestamp", "data"]):
                if data["type"] == EVENTS["NEW_CONVERSATION"]:
                    # Cria uma nova conversa
                    try:
                        conversation = create_open_conversation(
                            data["data"]["id"], data["timestamp"]
                        )
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
                        return JsonResponse(
                            {"status": "error", "message": error_message}, status=400
                        )
                elif data["type"] == EVENTS["NEW_MESSAGE"]:
                    # Adiciona uma mensagem à conversa
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
                        return JsonResponse(
                            {"status": "error", "message": error_message}, status=400
                        )
                    except Conversation.DoesNotExist:
                        return JsonResponse(
                            {"status": "error", "message": "Conversation not found"},
                            status=404,
                        )
                    except Exception as e:
                        return JsonResponse(
                            {"status": "error", "message": str(e)}, status=400
                        )
                elif data["type"] == EVENTS["CLOSE_CONVERSATION"]:
                    # Fecha uma conversa
                    print("entrou aqui ?")
                    try:
                        conversation = close_conversation(
                            data["data"]["id"], data["timestamp"]
                        )
                        
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
                            {"status": "error", "message": "Conversation not found"},
                            status=404,
                        )
                    except Exception as e:
                        return JsonResponse(
                            {"status": "error", "message": str(e)}, status=400
                        )
                else:
                    # Tipo inválido
                    return JsonResponse(
                        {
                            "status": "error",
                            "message": "Invalid type. Expected 'NEW_CONVERSATION' or 'NEW_MESSAGE'",
                        },
                        status=400,
                    )

            else:
                return JsonResponse(
                    {"status": "error", "message": "Invalid payload"}, status=400
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
