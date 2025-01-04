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


            def is_inappropriate(message):
                message_lower = message.lower()
                return any(keyword in message_lower for keyword in BLOCKED_KEYWORDS)

            if is_inappropriate(content):
                return Response({
                    "error": "Inappropriate message content.",
                    "response": "I'm here to assist with meaningful and respectful conversations."
                }, status=status.HTTP_400_BAD_REQUEST)

            # Check cache for sender and recipient
            sender = cache.get(f"user_{sender_id}")
            recipient = cache.get(f"user_{recipient_id}")

            if not sender or not recipient:
                users = db.query(User).filter(User.id.in_([sender_id, recipient_id])).all()
                if len(users) < 2:
                    return Response({"error": "Invalid sender or recipient."}, status=status.HTTP_400_BAD_REQUEST)
                for user in users:
                    cache.set(f"user_{user.id}", user, timeout=3600)

            # Save the message
            message = Message(sender_id=sender_id, recipient_id=recipient_id, content=content)
            db.add(message)
            db.commit()
            db.refresh(message)

            # Save the message in conversation history
            conversation_key = f"conversation_{min(sender_id, recipient_id)}_{max(sender_id, recipient_id)}"
            redis_client.lpush(conversation_key, f"User: {content}")
            redis_client.expire(conversation_key, 600)  # Set expiration to 10 minutes

            # Retrieve recent conversation history
            recent_history = redis_client.lrange(conversation_key, 0, -1)
            history_prompt = "\n".join(reversed(recent_history))

            # Fetch questionnaire answers
            questionnaire_answers = cache.get(f"questionnaire_{recipient_id}")
            if not questionnaire_answers:
                questionnaire_answers = db.query(Questionnaire.answer).filter(
                    Questionnaire.user_id == recipient_id
                ).all()
                cache.set(f"questionnaire_{recipient_id}", questionnaire_answers, timeout=3600)

            style_prompt = " ".join([q[0] for q in questionnaire_answers]) if questionnaire_answers else ""
            openai_prompt = f"Conversation history:\n{history_prompt}\nRespond to the last message: '{content}'. Use this user's style: {style_prompt}"

            # GPT System Prompt Refinement
            system_prompt = (
                "You are a digital assistant mimicking the user's style. "
                "Avoid answering personal questions like relationship status, age, or other sensitive topics. "
                "Focus on providing helpful and meaningful responses."
            )

            # Fetch GPT response
            def fetch_gpt_response():
                total_token_limit = 4096  
                prompt_tokens = len(openai_prompt.split())  
                max_tokens = min(100, total_token_limit - prompt_tokens) 

                return openai.ChatCompletion.create(
                    model="gpt-4o",
                    max_tokens=max_tokens,
                    temperature=0.3,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": openai_prompt},
                    ],
                )

            with ThreadPoolExecutor() as executor:
                future = executor.submit(fetch_gpt_response)
                response = future.result()
                generated_response = response['choices'][0]['message']['content']

            # Validate the AI response
            BLOCKED_PHRASES = ["I don't have a relationship status", "I'm just a virtual assistant"]
            def validate_response(response_text):
                for phrase in BLOCKED_PHRASES:
                    if phrase in response_text:
                        return "I'm here to assist with meaningful and respectful conversations."
                return response_text

            validated_response = validate_response(generated_response)

            # Save the AI's response to history
            redis_client.lpush(conversation_key, f"AI: {validated_response}")

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