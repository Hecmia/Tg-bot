from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Boolean, inspect
from sqlalchemy.orm import declarative_base, sessionmaker

# Базовое местоположение и подключение к базе данных
DATABASE_URL = 'sqlite:///G:/ttt/tg_bot/database.db'
engine = create_engine(DATABASE_URL)

# Определяем базовый класс
Base = declarative_base()


# Определяем модель
class Teachers(Base):
    __tablename__ = 'teachers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    subject = Column(String)
    email = Column(String, unique=True)


class ReviewsTeachers(Base):
    __tablename__ = 'reviews_teachers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    teacher_id = Column(Integer, ForeignKey('teachers.id'))
    strictness = Column(Integer)
    scope_of_work = Column(Integer)
    difficulty_of_delivery = Column(Integer)
    attitude_to_attending_classes = Column(Integer)
    keeps_his_word = Column(Integer)
    mercy = Column(Integer)
    the_subject = Column(String)
    is_approved = Column(Boolean, default=False)


Base.metadata.create_all(engine)