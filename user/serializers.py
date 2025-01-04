from rest_framework import serializers
from models.models_sqlalchemy import User, Questions, Questionnaire

class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=True)
    phone_number = serializers.CharField(required=True)
    age = serializers.IntegerField(required=False)
    sex = serializers.CharField(required=False)
    location = serializers.CharField(required=False)
    job_title = serializers.CharField(required=False)
    company_name = serializers.CharField(required=False)
    education = serializers.CharField(required=False)

class QuestionSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    text = serializers.CharField(required=True)

class QuestionnaireSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    user_id = serializers.IntegerField(required=True)
    question_id = serializers.IntegerField(required=True)
    answer = serializers.CharField(required=True)