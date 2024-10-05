from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

# Базовое местоположение и подключение к базе данных
DATABASE_URL = 'sqlite:///G:/ttt/tg_bot/database.db'
engine = create_engine(DATABASE_URL)

# Определяем базовый класс
Base = declarative_base()


# Определяем модель для таблицы teachers
class Teachers(Base):
    __tablename__ = 'teachers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    subjects = Column(String)
    groups = Column(String)
    department = Column(String)
    contacts = Column(String)


# Создаем сессию
Session = sessionmaker(bind=engine)
session = Session()

# Чтение всех записей из таблицы teachers
teachers = session.query(Teachers).all()
for teacher in teachers:
    print(f"ID: {teacher.id}, Name: {teacher.name}")

# Закрываем сессию
session.close()