from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .db import Base


class Student(Base):
    """Модель для представления ученика"""

    __tablename__ = "students"

    id = Column(Integer, primary_key=True)
    """Уникальный идентификатор ученика"""
    first_name = Column(String, nullable=False)
    """Имя ученика"""
    last_name = Column(String, nullable=False)
    """Фамилия ученика"""
    scores = relationship("Score", back_populates="student")
    """Связь с моделью Score, представляющая баллы ученика"""


class Score(Base):
    """Модель для представления баллов ученика по предметам"""

    __tablename__ = "scores"

    id = Column(Integer, primary_key=True)
    """Уникальный идентификатор балла"""
    subject = Column(String, nullable=False)
    """Название предмета"""
    score = Column(Integer, nullable=False)
    """Балл ученика по предмету"""
    student_id = Column(Integer, ForeignKey("students.id"))
    """Идентификатор ученика, которому принадлежат баллы"""
    student = relationship("Student", back_populates="scores")
    """Связь с моделью Student, представляющая ученика"""
