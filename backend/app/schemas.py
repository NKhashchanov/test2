from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List, Optional

# User schemas
class UserBase(BaseModel):
    email: EmailStr
    username: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Task Difficulty schemas
class TaskDifficultyBase(BaseModel):
    task_difficulty_name: str

class TaskDifficultyResponse(TaskDifficultyBase):
    task_difficulty_id: int

    class Config:
        from_attributes = True

# Task Theme schemas
class TaskThemeBase(BaseModel):
    task_theme_name: str

class TaskThemeResponse(TaskThemeBase):
    task_theme_id: int

    class Config:
        from_attributes = True

# Exercise schemas
class ExerciseBase(BaseModel):
    exercises_name: str
    description: Optional[str] = None
    task_difficulty_id: int
    task_theme_id: int
    query_template: str

class ExerciseCreate(ExerciseBase):
    pass

class ExerciseResponse(ExerciseBase):
    exercises_id: int
    created_at: datetime
    difficulty: Optional[TaskDifficultyResponse] = None
    theme: Optional[TaskThemeResponse] = None

    class Config:
        from_attributes = True

# User Exercise schemas
class UserExerciseBase(BaseModel):
    user_id: int
    exercise_id: int
    completed: bool
    user_query: str

class UserExerciseCreate(UserExerciseBase):
    pass

class UserExerciseResponse(UserExerciseBase):
    user_exercises_id: int
    completed_at: datetime
    user: Optional[UserResponse] = None
    exercise: Optional[ExerciseResponse] = None

    class Config:
        from_attributes = True

# Auth schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None