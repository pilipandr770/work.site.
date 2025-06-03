from app import create_app, db
from flask_migrate import Migrate, upgrade, init, migrate

app = create_app()
migrate_tool = Migrate(app, db)

with app.app_context():
    try:
        # Попробуем инициализировать миграцию если это первый запуск
        init()
    except:
        pass  # Если уже инициализировано, просто пропускаем
    
    # Создаём миграцию
    migrate(message='Добавлены модели для IT-магазина, токенов, аирдропа и DAO')
    
    # Применяем миграцию
    upgrade()

print("Миграция успешно создана и применена!")
