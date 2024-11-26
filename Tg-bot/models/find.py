from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
from models.create_reviews import ReviewsTeachers
from sqlalchemy import func
from sqlalchemy.future import select


DATABASE_URL = 'sqlite:///C:/Users/Алиса/PycharmProjects/Tg-bot/database/database.db'
engine = create_engine(DATABASE_URL)

Base = declarative_base()


class Teachers(Base):
    __tablename__ = 'teachers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    subjects = Column(String)
    groups = Column(String)
    department = Column(String)
    contacts = Column(String)


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


def get_reviews(teacher_name, subject):
    teacher_list = session.query(Teachers).join(ReviewsTeachers, ReviewsTeachers.teacher_id == Teachers.id).filter(
        Teachers.name.ilike(f"%{teacher_name}%"),
        ReviewsTeachers.is_approved == True
    ).all()

    if teacher_list:
        id = [teacher.id for teacher in teacher_list]
        reviews_list = session.query(ReviewsTeachers).filter(
            ReviewsTeachers.teacher_id.in_(id),
            ReviewsTeachers.the_subject.ilike(f"%{subject}%")
        ).all()
        teacher_name = teacher_list[0].name.strip()
        return reviews_list, teacher_name
    else:
        return [], teacher_name


def get_average_reviews(teacher_name: str, subject: str, session):
    try:
        teacher = session.query(Teachers).filter(Teachers.name.ilike(f"%{teacher_name}%")).first()

        if not teacher:
            return None

        result = session.execute(
            select(
                func.avg(ReviewsTeachers.strictness).label('avg_strictness'),
                func.avg(ReviewsTeachers.scope_of_work).label('avg_scope_of_work'),
                func.avg(ReviewsTeachers.difficulty_of_delivery).label('avg_difficulty_of_delivery'),
                func.avg(ReviewsTeachers.attitude_to_attending_classes).label('avg_attitude_to_attending_classes'),
                func.avg(ReviewsTeachers.keeps_his_word).label('avg_keeps_his_word'),
                func.avg(ReviewsTeachers.mercy).label('avg_mercy')
            )
            .filter(
                ReviewsTeachers.teacher_id == teacher.id,
                ReviewsTeachers.the_subject.ilike(f"%{subject}%"),
                ReviewsTeachers.is_approved == True
            )
        )

        averages = result.fetchone()

        if not averages or all(value is None for value in averages):
            return None

        return averages

    except Exception:
        return None



