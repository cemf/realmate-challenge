from conversations.models import Conversation, Message

def create_open_conversation(id, starting_date):
    conversation = Conversation.objects.create(
        id=id,
        status=Conversation.STATUS_OPEN,
        start_conversation_date=starting_date,
    )
    
    return conversation


def add_message_to_conversation(id, conversation_id, text, direction):   
    message = Message.objects.create(
        id=id,
        conversation_id=conversation_id,
        text=text,
        direction=direction,
    )
    return message


def get_conversation_by_id(id):
    try:
        conversation = Conversation.objects.get(id=id)
        return conversation
    except Conversation.DoesNotExist:
        return None

def get_message_by_id(id):
    try:
        message = Message.objects.get(id=id)
        return message
    except Message.DoesNotExist:
        return None
    
def close_conversation(conversation_id, ending_date):
    conversation = get_conversation_by_id(conversation_id)
    if conversation:
        conversation.status = Conversation.STATUS_CLOSED
        conversation.end_conversation_date = ending_date
        conversation.save()
        return conversation
    else:
        return None
