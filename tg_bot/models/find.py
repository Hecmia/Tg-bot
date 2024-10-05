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

def get_professor(teachers_find):
    teacher_list = session.query(Teachers).filter(Teachers.name.ilike(f"%{teachers_find}%")).all()

    if teacher_list:
        names = [teacher.name for teacher in teacher_list]
        id = [teacher.id for teacher in teacher_list]
        return {'name': names, 'id': id}
    else:
        return []


def get_subject(subject_find):
    subject_list = session.query(Teachers).filter(Teachers.subjects.ilike(f"%{subject_find}%")).first()

    if subject_list:
        sub_find = def_subject_find(subject_list, subject_find)
        return sub_find
    else:
        return []

def def_subject_find(subject_list, subject_find):
    subject_list = subject_list.subjects.split('\n')
    for subject in subject_list:
        if subject_find in subject:
            return subject

    return []