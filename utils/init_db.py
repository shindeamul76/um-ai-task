from database import engine
from models.models_sqlalchemy import Base

# Initialize Database
def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()