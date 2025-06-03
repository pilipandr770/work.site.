# Подключение к PostgreSQL для продакшена

## Текущая ситуация

- ✅ Приложение правильно работает с SQLite
- ✅ Модуль psycopg2-binary установлен
- ✅ PostgreSQL установлен и запущен на порту 5433
- ✅ Конфигурация приложения готова для обоих типов баз данных

## Шаги для подключения к PostgreSQL

### 1. Создание базы данных в PostgreSQL

Для создания базы данных можно использовать pgAdmin или командную строку:

```sql
CREATE DATABASE ittoken_db;
```

### 2. Проверка учетных данных PostgreSQL

Проверьте, что ваши учетные данные для PostgreSQL корректны:
- Имя пользователя: `postgres` (стандартный пользователь PostgreSQL)
- Пароль: Тот, который вы указали при установке PostgreSQL
- Порт: 5433 (не стандартный 5432, а именно 5433 - как показала проверка)

### 3. Настройка подключения в .env

Измените файл `.env`, раскомментировав строку с PostgreSQL и закомментировав SQLite:

```properties
SECRET_KEY=your-secret-key
# Для PostgreSQL (ваши данные):
DATABASE_URL=postgresql://postgres:Dnepr75ok6137707@localhost:5433/ittoken_db
# Для SQLite (раскомментируйте если нужно вернуться к SQLite):
# DATABASE_URL=sqlite:///C:/Users/ПК/ITTOKEN/instance/site.db
```

### 4. Инициализация базы данных PostgreSQL

После настройки подключения нужно создать таблицы:

```bash
python app/migrations_update.py
```

### 5. Создание демо-данных (опционально)

```bash
python app/create_demo_data.py
```

### 6. Запуск приложения с PostgreSQL

```bash
python -m app.run
```

## Проверка работоспособности

1. Убедитесь, что все страницы приложения работают
2. Проверьте операции с данными (регистрация, вход, и т.д.)
3. Убедитесь, что все данные сохраняются и извлекаются корректно

## Возможные проблемы и решения

### Ошибка: "psycopg2.OperationalError: FATAL: password authentication failed"
- Причина: неверный пароль
- Решение: проверьте пароль для пользователя PostgreSQL

### Ошибка: "psycopg2.OperationalError: connection refused"
- Причина: PostgreSQL не запущен или работает на другом порту
- Решение: проверьте, что сервис PostgreSQL запущен и слушает порт 5433

### Ошибка: "psycopg2.ProgrammingError: database ittoken_db does not exist"
- Причина: база данных не создана
- Решение: создайте базу данных в PostgreSQL

## Для развертывания на сервере

Для развертывания на сервере с PostgreSQL:

1. Убедитесь, что PostgreSQL установлен
2. Создайте базу данных и пользователя
3. Укажите DATABASE_URL в соответствующем формате
4. Используйте gunicorn для запуска приложения:
   ```bash
   gunicorn app.wsgi:app
   ```
