# Wildberries Feedback Collector

Сервис для сбора и сохранения **отрицательных отзывов** о товарах Wildberries.  
Вы указываете артикул товара, минимальный допустимый рейтинг и количество дней — скрипт получает свежие отзывы и сохраняет их в базу данных PostgreSQL.

---

## 🛠 Требования

- Python **3.10+**
- PostgreSQL **13+**
- Установленные зависимости (`requirements.txt`)

---

## ⚙️ Настройка проекта

1. Клонируйте репозиторий:

```bash
git clone <repo_url>
cd solution_test_case
```

2. Создайте и активируйте виртуальное окружение:

```bash
python -m venv venv
source venv/bin/activate   # Linux / Mac
venv\Scripts\activate      # Windows
```

3. Установите зависимости:

```bash
pip install -r requirements.txt
```

4. Настройте подключение к базе данных через файл **`.env`** (он уже есть в проекте):

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_DB=wb_feedbacks
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

---

## 🗄 Подготовка базы данных

1. Создайте базу данных:

```bash
psql -U postgres -h localhost -p 5432 -c "CREATE DATABASE wb_feedbacks;"
```

2. При первом запуске проект автоматически создаст нужные таблицы (через `app/database.py`).

---

## ▶️ Запуск

Запуск основного скрипта:

```bash
python main.py <nm> [--rating RATING] [--days DAYS]
```

### Аргументы:
- `nm` — артикул товара (обязательный).
- `--rating` — минимальный рейтинг, ниже которого отзыв считается «плохим» (по умолчанию `3`).
- `--days` — количество дней для фильтрации отзывов по дате (по умолчанию `3`).

---

## 📌 Примеры использования

### Собрать плохие отзывы за последние 3 дня (рейтинг < 3)
```bash
python main.py 12345678 --rating 3 --days 3
```

### Собрать плохие отзывы за последнюю неделю (рейтинг < 4)
```bash
python main.py 12345678 --rating 4 --days 7
```

После выполнения:
- В консоль будет выведено количество найденных отзывов.
- Все новые отзывы сохранятся в PostgreSQL (`wb_feedbacks`).

---

## 📝 Логи

Логи пишутся:
- в консоль (`stdout`)
- в файл: `logs/app.log` (ротация — до 5 файлов по 5 MB каждый).

---

## 📂 Архитектура проекта

```
project/
│── .env                  # Настройки БД
│── main.py               # Точка входа
│── requirements.txt      # Зависимости
│── app/
│   ├── logger.py
│   ├── database.py       # Подключение к БД
│   ├── models/           # Модели (SQLAlchemy + Pydantic)
│   │   ├── schemas.py
│   │   └── db.py
│   └── services/
│       └── wildberries_client.py  # Клиент WB API
