from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime, timezone

Base = declarative_base()

# User Table
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    phone_number = Column(String, unique=True, nullable=False)
    age = Column(Integer)
    sex = Column(String)
    location = Column(String)
    job_title = Column(String)
    company_name = Column(String)
    education = Column(String)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, onupdate=lambda: datetime.now(timezone.utc))

    questionnaires = relationship("Questionnaire", back_populates="user")
    user_questions = relationship("UserQuestions", back_populates="user")
    sent_messages = relationship("Message", foreign_keys="[Message.sender_id]", back_populates="sender")  
    received_messages = relationship("Message", foreign_keys="[Message.recipient_id]", back_populates="recipient")


# Questions Table
class Questions(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    user_questions = relationship("UserQuestions", back_populates="question")
    questionnaires = relationship("Questionnaire", back_populates="question")

# UserQuestions Table
class UserQuestions(Base):
    __tablename__ = "user_questions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    answered = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

   
    user = relationship("User", back_populates="user_questions")  # Relationship back to User
    question = relationship("Questions", back_populates="user_questions")  # Relationship back to Questions


# Questionnaire Table
class Questionnaire(Base):
    __tablename__ = "questionnaire"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    answer = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    user = relationship("User", back_populates="questionnaires")  
    question = relationship("Questions", back_populates="questionnaires") 



# Message Table
class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # Foreign key to User (sender)
    recipient_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # Foreign key to User (recipient)
    content = Column(String, nullable=False)  
    response = Column(String, nullable=True)  
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))  # Timestamp of the message


    sender = relationship("User", foreign_keys=[sender_id], back_populates="sent_messages")
    recipient = relationship("User", foreign_keys=[recipient_id], back_populates="received_messages")