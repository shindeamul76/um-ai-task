from utils.redis import redis_client
from sqlalchemy.orm import Session
from models.models_sqlalchemy import User, Questionnaire



def validate_inappropriate_content(content, blocked_keywords):
    """Check if the content contains blocked keywords."""
    content_lower = content.lower()
    return any(keyword in content_lower for keyword in blocked_keywords)



def validate_sender_recipient(db: Session, sender_id, recipient_id):
    """Validate sender and recipient from the database."""
    users = db.query(User).filter(User.id.in_([sender_id, recipient_id])).all()
    if len(users) < 2:
        return None
    return {user.id: user for user in users}




def fetch_questionnaire_answers(db: Session, recipient_id):
    """Fetch questionnaire answers for the recipient."""
    return db.query(Questionnaire.answer).filter(Questionnaire.user_id == recipient_id).all()



def manage_conversation_history(sender_id, recipient_id, content, action="save"):
    """
    Save or retrieve conversation history between two users.

    Args:
        sender_id (int): The ID of the sender.
        recipient_id (int): The ID of the recipient.
        content (str): The message content to be saved.
        action (str, optional): The action to perform, either "save" to store the message or "retrieve" to get the conversation history. Defaults to "save".

    Returns:
        list or None: If action is "retrieve", returns a list of messages in the conversation history. If action is "save", returns None.
    """
    """Save or retrieve conversation history."""
    conversation_key = f"conversation_{min(sender_id, recipient_id)}_{max(sender_id, recipient_id)}"
    if action == "save":
        redis_client.lpush(conversation_key, content)
        redis_client.expire(conversation_key, 600)
    elif action == "retrieve":
        return redis_client.lrange(conversation_key, 0, -1)
    return None