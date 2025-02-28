import datetime
import uuid
from django.db import models
from django.forms import ValidationError


# Create your models here.
class Conversation(models.Model):
    # Estados possíveis para uma conversa
    STATUS_OPEN = "OPEN"
    STATUS_CLOSED = "CLOSED"
    STATUS_CHOICES = [
        (STATUS_OPEN, "Open"),
        (STATUS_CLOSED, "Closed"),
    ]
    id = models.TextField(primary_key=True)
    start_conversation_date = models.DateTimeField(default=datetime.datetime.now)
    end_conversation_date = models.DateTimeField(default=None, null=True)

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=STATUS_OPEN,
    )

    def __str__(self):
        return f"Conversation {self.id} ({self.status})"


class Message(models.Model):
    # Tipos possíveis para uma mensagem

    TYPE_SENT = "SENT"
    TYPE_RECEIVED = "RECEIVED"
    TYPE_CHOICES = [
        (TYPE_SENT, "Sent"),
        (TYPE_RECEIVED, "Received"),
    ]
    id = models.TextField(primary_key=True)
    conversation_id = models.CharField(max_length=36)

    text = models.TextField()
    direction = models.CharField(
        max_length=10,
        choices=TYPE_CHOICES,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message {self.id} ({self.direction}) in {self.conversation_id}"

    def save(self, *args, **kwargs):
        # Busca a conversa pelo conversation_id
        try:
            conversation = Conversation.objects.get(id=self.conversation_id)
        except Conversation.DoesNotExist:
            raise ValidationError("Conversation does not exist.")

        # Verifica se a conversa está fechada
        if conversation.status == Conversation.STATUS_CLOSED:
            raise ValidationError("Cannot add messages to a closed conversation.")

        # Salva a mensagem
        super().save(*args, **kwargs)
