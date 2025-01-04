from django.core.management.base import BaseCommand
from sqlalchemy.orm import Session
from utils.database import get_db
from models.models_sqlalchemy import Questions


class Command(BaseCommand):
    help = "Populate the Questions table with default questions"

    def handle(self, *args, **kwargs):
        db = next(get_db()) 
        try:
            # Predefined questions
            questions = [
                "How do you introduce yourself to new people?",
                "What kind of people do you like to talk to?",
                "How would you politely decline an offer you’re not interested in?",
                "What's your favorite way to start a conversation?",
                "How do you respond to compliments?",
                "What are your hobbies and interests?",
                "What is your idea of a perfect date?",
                "What qualities do you look for in a partner?",
                "How do you spend your weekends?",
                "What is your favorite travel destination?",
                "What are your long-term goals?",
                "How do you handle conflicts in a relationship?",
                "What is your favorite book or movie?",
                "What is the most important thing you are looking for in a relationship?",
                "How do you like to spend your free time?",
            ]

            # Insert each question into the Questions table
            for question_text in questions:
                question = Questions(text=question_text)
                db.add(question)

            # Commit the transaction
            db.commit()

            self.stdout.write(self.style.SUCCESS("Successfully populated the Questions table."))

        finally:
            db.close()  # Ensure the session is closed