# Проблемы и решения для PostgreSQL с Flask

## Проблемы, которые могут возникнуть при подключении PostgreSQL с Flask

### 1. Ошибка ModuleNotFoundError: No module named 'psycopg2'

**Решение**:
```
pip install psycopg2-binary
```

Убедитесь, что установка выполняется в активированное виртуальное окружение:
```
# Активация виртуального окружения
(Windows) venv\Scripts\activate
(Linux/Mac) source venv/bin/activate

# Установка пакета
pip install psycopg2-binary
```

### 2. Ошибка подключения "connection refused"

**Возможные причины**:
- PostgreSQL не запущен
- Неверный порт (обычно 5432 или 5433)
- Файервол блокирует подключение

**Решение**:
- Запустите службу PostgreSQL (Windows: services.msc)
- Проверьте порт в файле postgresql.conf
- Проверьте настройки файервола

### 3. Ошибка аутентификации

**Возможные причины**:
- Неверное имя пользователя или пароль
- Неверные права доступа

**Решение**:
- Проверьте учетные данные
- Проверьте настройки в файле pg_hba.conf

### 4. База не существует

**Решение**:
```sql
CREATE DATABASE ittoken_db;
```

### 5. OperationalError без дополнительных сведений

**Решение**:
```python
# Добавьте отладочную информацию к строке подключения
try:
    db.session.execute('SELECT 1')
except Exception as e:
    print(f"Ошибка подключения: {str(e)}")
```

### 6. Ошибка SSL: "SSL SYSCALL error: EOF detected"

**Решение**:
```
# Добавьте параметр sslmode=disable к URL
postgresql://user:password@localhost/dbname?sslmode=disable
```

## Миграция данных из SQLite в PostgreSQL

Для миграции данных из SQLite в PostgreSQL используйте скрипт `migrate_to_postgres.py`:

```
python migrate_to_postgres.py
```

## Переключение между базами данных

### SQLite (для разработки)
```
# .env
DATABASE_URL=sqlite:///instance/site.db
```

### PostgreSQL (для продакшена)
```
# .env
DATABASE_URL=postgresql://postgres:password@localhost:5433/ittoken_db
```

## Проверка состояния базы данных

```python
python -c "from app import create_app, db; app = create_app(); with app.app_context(): print(db.engine.url)"
```
