from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from sqlalchemy.orm import Session
from utils.database import get_db
from utils.redis import redis_client
from models.models_sqlalchemy import Message, User, Questionnaire
from .serializers import MessageSerializer
import openai
from django.conf import settings
from concurrent.futures import ThreadPoolExecutor
from django.core.cache import cache
from utils.blocked_questions import BLOCKED_KEYWORDS
from .utils.openai_handler import generate_prompt, fetch_gpt_response
from .utils.utils import (
    validate_inappropriate_content,
    validate_sender_recipient,
    fetch_questionnaire_answers,
    manage_conversation_history,
)



openai.api_key = settings.OPENAI_API_KEY


class MessageView(APIView):
    """
    POST /messages/
    Send a message and generate a response using GPT.
    GET /messages/<user_id>/
    Retrieve message history for a user.
    """

    def post(self, request):
        db = next(get_db())
        try:
            sender_id = request.data.get("sender_id")
            recipient_id = request.data.get("recipient_id")
            content = request.data.get("content")

            # Validate inappropriate content
            if validate_inappropriate_content(content, BLOCKED_KEYWORDS):
                return Response({
                    "error": "Inappropriate message content.",
                    "response": "I'm here to assist with meaningful and respectful conversations."
                }, status=status.HTTP_400_BAD_REQUEST)

            # Validate sender and recipient
            users = validate_sender_recipient(db, sender_id, recipient_id)
            if not users:
                return Response({"error": "Invalid sender or recipient."}, status=status.HTTP_400_BAD_REQUEST)
            sender, recipient = users[sender_id], users[recipient_id]

            # Save the message
            message = Message(sender_id=sender_id, recipient_id=recipient_id, content=content)
            db.add(message)
            db.commit()
            db.refresh(message)

            # Save the message to conversation history
            manage_conversation_history(sender_id, recipient_id, f"User: {content}", action="save")

            # Retrieve conversation history
            recent_history = manage_conversation_history(sender_id, recipient_id, content=None, action="retrieve")
            history_prompt = "\n".join(reversed(recent_history))

            # Fetch questionnaire answers
            questionnaire_answers = cache.get(f"questionnaire_{recipient_id}")
            if not questionnaire_answers:
                questionnaire_answers = fetch_questionnaire_answers(db, recipient_id)
                cache.set(f"questionnaire_{recipient_id}", questionnaire_answers, timeout=3600)

            style_prompt = " ".join([q[0] for q in questionnaire_answers]) if questionnaire_answers else ""

            # Generate OpenAI prompt
            openai_prompt = generate_prompt(history_prompt, content, style_prompt)

            # Fetch GPT response
            with ThreadPoolExecutor() as executor:
                future = executor.submit(fetch_gpt_response, openai_prompt)
                generated_response = future.result()

            # Validate the AI response
            BLOCKED_PHRASES = ["I don't have a relationship status", "I'm just a virtual assistant"]
            validated_response = generated_response
            for phrase in BLOCKED_PHRASES:
                if phrase in generated_response:
                    validated_response = "I'm here to assist with meaningful and respectful conversations."

            # Save the AI's response to history
            manage_conversation_history(sender_id, recipient_id, f"AI: {validated_response}", action="save")

            # Update the database with the response
            message.response = validated_response
            db.commit()

            return Response({
                "message_id": message.id,
                "sender_id": sender_id,
                "recipient_id": recipient_id,
                "content": content,
                "response": validated_response
            }, status=status.HTTP_201_CREATED)
        finally:
            db.close()



    def get(self, request, user_id=None):
        db = next(get_db())  # Get SQLAlchemy session
        try:
            # Fetch message history for the user
            if not user_id:
                return Response(
                    {"error": "User ID is required in the URL path."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            messages = db.query(Message).filter(
                (Message.sender_id == user_id) | (Message.recipient_id == user_id)
            ).all()

            # Serialize the data
            serializer = MessageSerializer(messages, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            # Handle unexpected errors and log them
            error_message = str(e)
            return Response(
                {"error": "An unexpected error occurred.", "details": error_message},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        finally:
            db.close()  # Ensure the session is closed