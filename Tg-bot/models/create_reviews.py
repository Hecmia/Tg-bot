from sqlalchemy import create_engine, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import declarative_base, Mapped, mapped_column, relationship

DATABASE_URL = 'sqlite:///C:/Users/Алиса/PycharmProjects/Tg-bot/database/database.db'
engine = create_engine(DATABASE_URL)

Base = declarative_base()


class Teachers(Base):
    __tablename__ = 'teachers'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    subject: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    reviews: Mapped["ReviewsTeachers"] = relationship("ReviewsTeachers", back_populates="teacher")

    def __repr__(self) -> str:
        return f"<Teacher(id={self.id!r}, name={self.name!r}, subject={self.subject!r}, email={self.email!r})>"


class ReviewsTeachers(Base):
    __tablename__ = 'reviews_teachers'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    teacher_id: Mapped[int] = mapped_column(ForeignKey('teachers.id', ondelete="CASCADE"))
    strictness: Mapped[int] = mapped_column(Integer, nullable=False)
    scope_of_work: Mapped[int] = mapped_column(Integer, nullable=False)
    difficulty_of_delivery: Mapped[int] = mapped_column(Integer, nullable=False)
    attitude_to_attending_classes: Mapped[int] = mapped_column(Integer, nullable=False)
    keeps_his_word: Mapped[int] = mapped_column(Integer, nullable=False)
    mercy: Mapped[int] = mapped_column(Integer, nullable=False)
    the_subject: Mapped[str] = mapped_column(String, nullable=False)
    is_approved: Mapped[bool] = mapped_column(Boolean, default=False)
    note: Mapped[str] = mapped_column(String, nullable=False)

    teacher: Mapped["Teachers"] = relationship("Teachers", back_populates="reviews")

    def __repr__(self) -> str:
        return (f"<ReviewTeacher(id={self.id!r}, teacher_id={self.teacher_id!r}, strictness={self.strictness!r}, "
                f"scope_of_work={self.scope_of_work!r}, difficulty_of_delivery={self.difficulty_of_delivery!r}, "
                f"attitude_to_attending_classes={self.attitude_to_attending_classes!r})>")


class ReviewsBot(Base):
    __tablename__ = 'reviews_bot'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    creater: Mapped[int] = mapped_column(Integer, nullable=False)
    review: Mapped[str] = mapped_column(String, nullable=False)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)

    def __repr__(self) -> str:
        return f"<ReviewBot(id={self.id!r}, creater={self.creater!r}, review={self.review!r}, is_deleted={self.is_deleted!r})>"


Base.metadata.create_all(engine)