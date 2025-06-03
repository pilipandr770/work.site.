# Миграция с SQLite на PostgreSQL

## Что было изменено

1. **Добавлен PostgreSQL драйвер**: 
   - `psycopg2-binary` добавлен в `requirements.txt` и `app/requirements.txt`

2. **Обновлена конфигурация базы данных** в `app/config.py`:
   - Автоматическое определение типа БД через переменную окружения `DATABASE_URL`
   - Поддержка Heroku PostgreSQL (автоматическое исправление URL)
   - Fallback к SQLite для разработки

3. **Обновлен `.env.example`** с примерами конфигурации PostgreSQL

## Как использовать

### Для разработки (SQLite)
Оставьте `DATABASE_URL` пустой в `.env` или не устанавливайте её вообще:
```bash
# DATABASE_URL не задана - будет использоваться SQLite
```

### Для продакшена (PostgreSQL)
Установите `DATABASE_URL` в `.env`:
```bash
DATABASE_URL=postgresql://username:password@localhost:5432/ittoken_db
```

### Для Heroku
Heroku автоматически установит `DATABASE_URL`. Конфигурация автоматически исправит формат URL.

## Миграция данных

1. **Экспорт данных из SQLite** (если нужно сохранить существующие данные):
```bash
python -c "
from app import create_app, db
from app.models import *
import json

app = create_app()
with app.app_context():
    # Экспорт пользователей
    users = User.query.all()
    users_data = [{'username': u.username, 'email': u.email, 'is_admin': u.is_admin} for u in users]
    
    with open('users_backup.json', 'w') as f:
        json.dump(users_data, f, indent=2)
    
    print(f'Экспортировано {len(users)} пользователей')
"
```

2. **Настройка PostgreSQL**:
```bash
# Создайте базу данных PostgreSQL
createdb ittoken_db

# Установите DATABASE_URL
export DATABASE_URL=postgresql://username:password@localhost:5432/ittoken_db
```

3. **Инициализация новой базы**:
```bash
python app/migrations_update.py
```

4. **Создание демо-данных** (опционально):
```bash
python app/create_demo_data.py
```

## Проверка миграции

Запустите приложение и убедитесь, что:
- Все таблицы созданы корректно
- Регистрация/авторизация работает
- Магазин функционирует
- Блокчейн интеграция работает

## Rollback к SQLite

Если нужно вернуться к SQLite, просто удалите или закомментируйте `DATABASE_URL` в переменных окружения.
