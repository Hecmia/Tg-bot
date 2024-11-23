from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = 'sqlite:///G:/ttt/tg_bot/database.db'
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)