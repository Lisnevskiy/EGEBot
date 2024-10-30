from .db import Base, engine
from .models import Score, Student  # Импортируем модели для создания таблиц

# Создание таблиц в базе данных
Base.metadata.create_all(engine)
