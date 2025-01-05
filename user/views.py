from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from sqlalchemy.orm import Session
from utils.database import get_db
from models.models_sqlalchemy import User, Questions, UserQuestions
from .serializers import UserSerializer, QuestionSerializer, Questionnaire, UpdateUserSerializer
import random


class UserCreateView(APIView):
    """
    POST /users/
    Create a new user.
    """
    def post(self, request):
        db = next(get_db()) 
        try:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                data = serializer.validated_data
                
                # Check if phone_number already exists
                existing_user = db.query(User).filter_by(phone_number=data['phone_number']).first()
                if existing_user:
                    return Response(
                        {"error": "A user with this phone number already exists."},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                # Proceed with user creation
                new_user = User(**data) 
                db.add(new_user)  
                db.commit()  
                db.refresh(new_user)  
                return Response(UserSerializer(new_user).data, status=status.HTTP_201_CREATED)
            
            # If validation fails
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        finally:
            db.close()   



class UserListView(APIView):
    """
    GET /users/
    Retrieve all users.
    """
    def get(self, request):
        db = next(get_db())  # Retrieve the session instance from the generator
        try:
            users = db.query(User).all()  # Query the User model
            serializer = UserSerializer(users, many=True)  # Serialize the data
            return Response(serializer.data, status=status.HTTP_200_OK)
        finally:
            db.close()  # Explicitly close the session to ensure cleanup


class UserDetailView(APIView):
    """
    GET /users/<user_id>/
    Retrieve a single user by ID.
    """
    def get(self, request, user_id):
        db = next(get_db())  # Get the session from the generator
        try:
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        finally:
            db.close()  # Ensure the session is closed

    """
    PUT /users/<user_id>/
    Update a user by ID.
    """
    def patch(self, request, user_id):
        db = next(get_db())  # Get the session from the generator
        try:
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

            serializer = UpdateUserSerializer(user, data=request.data)
            if serializer.is_valid():
                for key, value in serializer.validated_data.items():
                    setattr(user, key, value)
                db.commit()
                db.refresh(user)
                return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        finally:
            db.close()  # Ensure the session is closed

    """
    DELETE /users/<user_id>/
    Delete a user by ID.
    """
    def delete(self, request, user_id):
        db = next(get_db())  # Get the session from the generator
        try:
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

            db.delete(user)
            db.commit()
            return Response({"message": "User deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        finally:
            db.close()  # Ensure the session is closed


class FetchQuestionsView(APIView):
    """
    GET /users/<user_id>/questions/
    Fetch 15 random questions that the user has not answered yet.
    """
    def get(self, request, user_id):
        db = next(get_db())  # Get the session from the generator
        try:
            # Fetch all questions the user has already answered
            answered_questions = db.query(UserQuestions).filter(UserQuestions.user_id == user_id).all()
            answered_ids = {uq.question_id for uq in answered_questions}

            # Fetch all unanswered questions
            questions = db.query(Questions).filter(~Questions.id.in_(answered_ids)).all()

            # Randomly select up to 15 questions
            random.shuffle(questions)
            selected_questions = questions[:15]

            # Mark these questions as assigned to the user
            for question in selected_questions:
                db.add(UserQuestions(user_id=user_id, question_id=question.id))
            db.commit()

            # Serialize and return the selected questions
            serializer = QuestionSerializer(selected_questions, many=True)
            return Response(serializer.data, status=200)
        finally:
            db.close()  # Ensure the session is closed
            

class SubmitResponsesView(APIView):
    """
    POST /users/<user_id>/responses/
    Submit answers to questions.
    """
    def post(self, request, user_id):
        db = next(get_db())  # Get the session from the generator
        try:
            responses = request.data

            if not isinstance(responses, list):
                return Response({"error": "Invalid data format. Expected a list of responses."},
                                status=status.HTTP_400_BAD_REQUEST)

            for response in responses:
                question_id = response.get("question_id")
                answer = response.get("answer")

                # Validate that the question has been assigned to the user
                user_question = db.query(UserQuestions).filter(
                    UserQuestions.user_id == user_id,
                    UserQuestions.question_id == question_id
                ).first()

                if not user_question:
                    return Response({"error": f"Question {question_id} not assigned to user {user_id}."},
                                    status=status.HTTP_400_BAD_REQUEST)

                # Save the response in the Questionnaire table
                db.add(Questionnaire(user_id=user_id, question_id=question_id, answer=answer))

                # Mark the question as answered
                user_question.answered = True

            db.commit()
            return Response({"message": "Responses saved successfully."}, status=status.HTTP_201_CREATED)
        finally:
            db.close()  # Ensure the session is closed