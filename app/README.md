# Инструкция по запуску проекта

## Необходимые компоненты:
- Python 3.10 или новее
- Node.js и npm (для компиляции смарт-контрактов)
- MetaMask кошелек для тестирования blockchain-функционала

## Шаг 1: Установка зависимостей

```bash
# Создание и активация виртуального окружения (если еще не создано)
python -m venv venv
# Для Windows
venv\Scripts\activate
# Для Linux/Mac
# source venv/bin/activate

# Установка зависимостей
pip install -r requirements.txt
```

## Шаг 2: Настройка переменных окружения

Создайте файл `.env` в корне проекта (если еще не создан) с следующими параметрами:

```
SECRET_KEY=ваш_секретный_ключ
DATABASE_URL=sqlite:///site.db
OPENAI_API_KEY=ваш_ключ_openai
OPENAI_ASSISTANT_ID=ваш_id_ассистента
POLYGON_PRIVATE_KEY=ваш_приватный_ключ_polygon
INFURA_API_KEY=ваш_ключ_infura
```

## Шаг 3: Создание базы данных и таблиц

```bash
python migrations_update.py
```

## Шаг 4: Создание демо-данных

```bash
python create_demo_data.py
```

## Шаг 5: Деплой смарт-контрактов (необязательно на этапе разработки)

```bash
python deploy_contracts.py
```

## Шаг 6: Запуск приложения

Для разработки:
```bash
python run.py
```

Для продакшна с использованием Gunicorn:
```bash
gunicorn wsgi:application
```

## Доступ к веб-приложению

После запуска приложение будет доступно по адресу http://127.0.0.1:5000

## Доступ в админ-панель

Логин: admin
Пароль: admin

## Структура проекта

- **admin/** - Модуль администрирования сайта
- **assist/** - Модуль ассистента на базе OpenAI
- **blockchain/** - Модуль для работы с блокчейн-функциями (токен, аирдроп, DAO)
- **contracts/** - Смарт-контракты Solidity
- **main/** - Основной модуль с главными страницами
- **shop/** - Модуль магазина
- **static/** - Статические файлы (CSS, JS, изображения)
- **templates/** - Шаблоны HTML
- **translations/** - Файлы переводов
- **utils/** - Вспомогательные утилиты
