#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Экспорт данных из SQLite в PostgreSQL.
Данный скрипт позволяет экспортировать данные из базы SQLite
в базу PostgreSQL для продакшена.
"""

import os
import sys
import json
import sqlite3
import time
from datetime import datetime

# Добавляем текущий каталог в путь для импорта
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    import psycopg2
    from psycopg2.extras import Json
    print("✅ Модуль psycopg2 успешно импортирован")
except ImportError:
    print("❌ Модуль psycopg2 не установлен!")
    print("Установите его командой: pip install psycopg2-binary")
    sys.exit(1)

# Чтение переменных окружения из .env файла
def load_dotenv():
    env_vars = {}
    try:
        with open('.env', 'r') as f:
            for line in f:
                if line.strip() and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    env_vars[key] = value
        print("✅ Переменные окружения загружены из .env")
        return env_vars
    except Exception as e:
        print(f"❌ Ошибка при чтении .env файла: {e}")
        return {}

# Подключение к SQLite
def connect_sqlite(db_path):
    try:
        print(f"Подключение к SQLite базе данных: {db_path}")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        return conn
    except Exception as e:
        print(f"❌ Ошибка подключения к SQLite: {e}")
        sys.exit(1)

# Подключение к PostgreSQL
def connect_postgres(db_url):
    try:
        print(f"Подключение к PostgreSQL: {db_url}")
        conn = psycopg2.connect(db_url)
        return conn
    except Exception as e:
        print(f"❌ Ошибка подключения к PostgreSQL: {e}")
        sys.exit(1)

# Получение списка таблиц из SQLite
def get_sqlite_tables(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row[0] for row in cursor.fetchall() 
              if row[0] != 'sqlite_sequence' and not row[0].startswith('sqlite_')]
    cursor.close()
    return tables

# Получение данных из таблицы SQLite
def get_sqlite_data(conn, table):
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table};")
    data = [dict(row) for row in cursor.fetchall()]
    cursor.close()
    return data

# Получение структуры таблицы SQLite
def get_sqlite_structure(conn, table):
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({table});")
    columns = [row['name'] for row in cursor.fetchall()]
    cursor.close()
    return columns

# Создание таблицы в PostgreSQL
def create_postgres_table(pg_conn, table_name, columns):
    try:
        cursor = pg_conn.cursor()
        
        # Формируем SQL для создания таблицы
        column_defs = []
        for col in columns:
            if col.lower() == 'id':
                column_defs.append(f"{col} SERIAL PRIMARY KEY")
            else:
                column_defs.append(f"{col} TEXT")
        
        create_sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(column_defs)});"
        
        cursor.execute(create_sql)
        pg_conn.commit()
        cursor.close()
        print(f"✅ Таблица {table_name} создана или уже существует")
        return True
    except Exception as e:
        print(f"❌ Ошибка создания таблицы {table_name}: {e}")
        return False

# Импорт данных в PostgreSQL
def import_data_to_postgres(pg_conn, table_name, columns, data):
    try:
        cursor = pg_conn.cursor()
        
        # Очистка таблицы перед импортом
        cursor.execute(f"TRUNCATE TABLE {table_name} RESTART IDENTITY CASCADE;")
        
        # Импорт данных
        for row in data:
            values = [row.get(col, None) for col in columns]
            placeholders = ', '.join(['%s' for _ in columns])
            insert_sql = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders});"
            cursor.execute(insert_sql, values)
        
        pg_conn.commit()
        cursor.close()
        print(f"✅ Импортировано {len(data)} записей в таблицу {table_name}")
        return True
    except Exception as e:
        print(f"❌ Ошибка импорта данных в таблицу {table_name}: {e}")
        pg_conn.rollback()
        return False

# Основная функция миграции
def migrate_sqlite_to_postgres():
    print("=" * 60)
    print("МИГРАЦИЯ ДАННЫХ ИЗ SQLITE В POSTGRESQL")
    print("=" * 60)
    
    # Загрузка переменных окружения
    env_vars = load_dotenv()
    
    # Получаем путь к SQLite базе
    sqlite_path = input("Введите путь к файлу SQLite базы (по умолчанию: instance/site.db): ")
    if not sqlite_path:
        sqlite_path = "instance/site.db"
    
    # Полный путь к SQLite базе
    full_sqlite_path = os.path.join(os.getcwd(), sqlite_path)
    if not os.path.exists(full_sqlite_path):
        print(f"❌ Файл базы данных не найден: {full_sqlite_path}")
        return
    
    # Получаем URL для PostgreSQL
    pg_url = input("Введите URL для PostgreSQL (например, postgresql://postgres:password@localhost:5433/ittoken_db): ")
    if not pg_url:
        # Используем значение из .env, если оно есть
        pg_url = env_vars.get('DATABASE_URL', '')
        if not pg_url or not pg_url.startswith('postgresql'):
            print("❌ URL PostgreSQL не задан")
            return
    
    # Подключаемся к базам
    sqlite_conn = connect_sqlite(full_sqlite_path)
    pg_conn = connect_postgres(pg_url)
    
    # Получаем список таблиц
    tables = get_sqlite_tables(sqlite_conn)
    print(f"\nНайдено {len(tables)} таблиц в SQLite базе:")
    for i, table in enumerate(tables):
        print(f"{i+1}. {table}")
    
    # Спрашиваем, какие таблицы мигрировать
    selected = input("\nВыберите номера таблиц для миграции (через запятую) или 'all' для всех: ")
    
    tables_to_migrate = []
    if selected.lower() == 'all':
        tables_to_migrate = tables
    else:
        try:
            indices = [int(idx.strip()) - 1 for idx in selected.split(',')]
            tables_to_migrate = [tables[idx] for idx in indices if 0 <= idx < len(tables)]
        except (ValueError, IndexError):
            print("❌ Неверный ввод. Используем все таблицы.")
            tables_to_migrate = tables
    
    print(f"\nБудут мигрированы следующие таблицы: {', '.join(tables_to_migrate)}")
    confirm = input("Продолжить? (y/n): ")
    if confirm.lower() != 'y':
        print("Миграция отменена.")
        return
    
    # Выполняем миграцию
    for table in tables_to_migrate:
        print(f"\nМиграция таблицы {table}...")
        columns = get_sqlite_structure(sqlite_conn, table)
        data = get_sqlite_data(sqlite_conn, table)
        
        if create_postgres_table(pg_conn, table, columns):
            import_data_to_postgres(pg_conn, table, columns, data)
    
    # Закрываем соединения
    sqlite_conn.close()
    pg_conn.close()
    
    print("\n" + "=" * 60)
    print("МИГРАЦИЯ ЗАВЕРШЕНА")
    print("=" * 60)
    print("\nТеперь вы можете изменить DATABASE_URL в .env файле на PostgreSQL.")
    
if __name__ == "__main__":
    migrate_sqlite_to_postgres()
