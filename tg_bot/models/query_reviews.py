from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base

# Базовое местоположение и подключение к базе данных
DATABASE_URL = 'sqlite:///G:/ttt/tg_bot/database.db'
engine = create_engine(DATABASE_URL)

# Определяем базовый класс
Base = declarative_base()


# Определяем модель для таблицы reviews_teachers
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


# Создаем сессию
Session = sessionmaker(bind=engine)
session = Session()

# Чтение всех записей из таблицы reviews_teachers
reviews = session.query(ReviewsTeachers).all()
for review in reviews:
    print(f"ID: {review.id}, Teacher ID: {review.teacher_id}, Strictness: {review.strictness}")

# Закрываем сессию
session.close()