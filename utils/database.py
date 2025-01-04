from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from django.conf import settings

DATABASE_URL = settings.SQLALCHEMY_DATABASE_URL

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db  
    finally:
        db.close()