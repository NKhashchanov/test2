from sqlalchemy.orm import Session
from . import models

def create_initial_data(db: Session):
    # Создаем сложности заданий
    difficulties = [
        models.TaskDifficulty(task_difficulty_name="Легкий"),
        models.TaskDifficulty(task_difficulty_name="Средний"),
        models.TaskDifficulty(task_difficulty_name="Сложный")
    ]
    
    for difficulty in difficulties:
        db.add(difficulty)
    db.commit()
    
    # Создаем темы заданий
    themes = [
        models.TaskTheme(task_theme_name="SELECT запросы"),
        models.TaskTheme(task_theme_name="JOIN операции"),
        models.TaskTheme(task_theme_name="Агрегатные функции")
    ]
    
    for theme in themes:
        db.add(theme)
    db.commit()
    
    # Создаем примеры заданий
    exercises = [
        models.Exercise(
            exercises_name="Базовый SELECT",
            description="Напишите запрос для выбора всех пользователей из таблицы users",
            task_difficulty_id=1,
            task_theme_id=1,
            query_template="SELECT * FROM users;"
        ),
        models.Exercise(
            exercises_name="Фильтрация данных",
            description="Напишите запрос для выбора пользователей с email содержащим 'gmail.com'",
            task_difficulty_id=2,
            task_theme_id=1,
            query_template="SELECT * FROM users WHERE email LIKE '%gmail.com%';"
        )
    ]
    
    for exercise in exercises:
        db.add(exercise)
    db.commit()
    
    print("Initial data created successfully!")