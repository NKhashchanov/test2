from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Связь с user_exercises
    exercises = relationship("UserExercise", back_populates="user")

class TaskDifficulty(Base):
    __tablename__ = "task_difficulty"

    task_difficulty_id = Column(Integer, primary_key=True, index=True)
    task_difficulty_name = Column(Text, unique=True, nullable=False)

    # Связь с exercises
    exercises = relationship("Exercise", back_populates="difficulty")

class TaskTheme(Base):
    __tablename__ = "task_theme"

    task_theme_id = Column(Integer, primary_key=True, index=True)
    task_theme_name = Column(Text, unique=True, nullable=False)

    # Связь с exercises
    exercises = relationship("Exercise", back_populates="theme")

class Exercise(Base):
    __tablename__ = "exercises"

    exercises_id = Column(Integer, primary_key=True, index=True)
    exercises_name = Column(Text, unique=True, nullable=False)
    description = Column(Text)
    task_difficulty_id = Column(Integer, ForeignKey("task_difficulty.task_difficulty_id"), nullable=False)
    task_theme_id = Column(Integer, ForeignKey("task_theme.task_theme_id"), nullable=False)
    query_template = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Связи
    difficulty = relationship("TaskDifficulty", back_populates="exercises")
    theme = relationship("TaskTheme", back_populates="exercises")
    user_exercises = relationship("UserExercise", back_populates="exercise")

class UserExercise(Base):
    __tablename__ = "user_exercises"

    user_exercises_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    exercise_id = Column(Integer, ForeignKey("exercises.exercises_id"), nullable=False)
    completed = Column(Boolean, nullable=False)
    completed_at = Column(DateTime, default=datetime.utcnow)
    user_query = Column(Text, nullable=False)

    # Связи
    user = relationship("User", back_populates="exercises")
    exercise = relationship("Exercise", back_populates="user_exercises")