from sqlalchemy.orm import sessionmaker
from src.models.user import db

def get_session():
    Session = sessionmaker(bind=db)
    session = Session()
    return session