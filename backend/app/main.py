from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from . import models, schemas
from .database import engine, get_db

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="SQL Exercises API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Создаем начальные данные
@app.on_event("startup")
def startup_event():
    db = next(get_db())
    try:
        # Проверяем, есть ли уже данные
        if db.query(models.TaskDifficulty).count() == 0:
            create_initial_data(db)
        print("Database initialized successfully!")
    except Exception as e:
        print(f"Error initializing database: {e}")
    finally:
        db.close()

@app.get("/")
async def root():
    return {"message": "SQL Exercises API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# User endpoints
@app.post("/users/", response_model=schemas.UserResponse)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    db_user = db.query(models.User).filter(
        (models.User.email == user.email) | (models.User.username == user.username)
    ).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email or username already registered")
    
    # In real app, hash the password
    # For now, we'll just store it as is (not secure - implement hashing in production)
    db_user = models.User(
        email=user.email,
        username=user.username,
        hashed_password=user.password  # Hash this in production!
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

@app.get("/users/", response_model=List[schemas.UserResponse])
async def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users

# Task Difficulty endpoints
@app.post("/task-difficulties/", response_model=schemas.TaskDifficultyResponse)
async def create_task_difficulty(
    difficulty: schemas.TaskDifficultyBase, 
    db: Session = Depends(get_db)
):
    db_difficulty = db.query(models.TaskDifficulty).filter(
        models.TaskDifficulty.task_difficulty_name == difficulty.task_difficulty_name
    ).first()
    if db_difficulty:
        raise HTTPException(status_code=400, detail="Task difficulty already exists")
    
    db_difficulty = models.TaskDifficulty(**difficulty.dict())
    db.add(db_difficulty)
    db.commit()
    db.refresh(db_difficulty)
    
    return db_difficulty

@app.get("/task-difficulties/", response_model=List[schemas.TaskDifficultyResponse])
async def get_task_difficulties(db: Session = Depends(get_db)):
    difficulties = db.query(models.TaskDifficulty).all()
    return difficulties

# Task Theme endpoints
@app.post("/task-themes/", response_model=schemas.TaskThemeResponse)
async def create_task_theme(theme: schemas.TaskThemeBase, db: Session = Depends(get_db)):
    db_theme = db.query(models.TaskTheme).filter(
        models.TaskTheme.task_theme_name == theme.task_theme_name
    ).first()
    if db_theme:
        raise HTTPException(status_code=400, detail="Task theme already exists")
    
    db_theme = models.TaskTheme(**theme.dict())
    db.add(db_theme)
    db.commit()
    db.refresh(db_theme)
    
    return db_theme

@app.get("/task-themes/", response_model=List[schemas.TaskThemeResponse])
async def get_task_themes(db: Session = Depends(get_db)):
    themes = db.query(models.TaskTheme).all()
    return themes

# Exercise endpoints
@app.post("/exercises/", response_model=schemas.ExerciseResponse)
async def create_exercise(exercise: schemas.ExerciseCreate, db: Session = Depends(get_db)):
    # Check if exercise name already exists
    db_exercise = db.query(models.Exercise).filter(
        models.Exercise.exercises_name == exercise.exercises_name
    ).first()
    if db_exercise:
        raise HTTPException(status_code=400, detail="Exercise name already exists")
    
    db_exercise = models.Exercise(**exercise.dict())
    db.add(db_exercise)
    db.commit()
    db.refresh(db_exercise)
    
    return db_exercise

@app.get("/exercises/", response_model=List[schemas.ExerciseResponse])
async def get_exercises(db: Session = Depends(get_db)):
    exercises = db.query(models.Exercise).all()
    return exercises

@app.get("/exercises/{exercise_id}", response_model=schemas.ExerciseResponse)
async def get_exercise(exercise_id: int, db: Session = Depends(get_db)):
    exercise = db.query(models.Exercise).filter(models.Exercise.exercises_id == exercise_id).first()
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")
    return exercise

# User Exercise endpoints
@app.post("/user-exercises/", response_model=schemas.UserExerciseResponse)
async def create_user_exercise(
    user_exercise: schemas.UserExerciseCreate, 
    db: Session = Depends(get_db)
):
    db_user_exercise = models.UserExercise(**user_exercise.dict())
    db.add(db_user_exercise)
    db.commit()
    db.refresh(db_user_exercise)
    
    return db_user_exercise

@app.get("/user-exercises/", response_model=List[schemas.UserExerciseResponse])
async def get_user_exercises(db: Session = Depends(get_db)):
    user_exercises = db.query(models.UserExercise).all()
    return user_exercises

@app.get("/user-exercises/user/{user_id}", response_model=List[schemas.UserExerciseResponse])
async def get_user_exercises_by_user(user_id: int, db: Session = Depends(get_db)):
    user_exercises = db.query(models.UserExercise).filter(
        models.UserExercise.user_id == user_id
    ).all()
    return user_exercises

@app.get("/debug/data")
async def debug_data(db: Session = Depends(get_db)):
    """Эндпоинт для отладки - проверяем наличие данных"""
    difficulties_count = db.query(models.TaskDifficulty).count()
    themes_count = db.query(models.TaskTheme).count()
    exercises_count = db.query(models.Exercise).count()
    users_count = db.query(models.User).count()
    
    return {
        "difficulties_count": difficulties_count,
        "themes_count": themes_count,
        "exercises_count": exercises_count,
        "users_count": users_count,
        "difficulties": db.query(models.TaskDifficulty).all(),
        "themes": db.query(models.TaskTheme).all(),
        "exercises": db.query(models.Exercise).all()
    }