# Battery Testing System

Приложение для управления и мониторинга процесса тестирования аккумуляторных элементов и батарей с использованием оборудования **Neware**.

## Описание

Проект представляет собой систему для работы с аппаратурой Neware, предназначенную для:
- Учета и отслеживания тестируемых ячеек (cells) и батарей (batteries)
- Хранения результатов тестирования (емкость, время заряда/разряда, дата теста)
- Привязки изделий к моделям продукции с техническими характеристиками

## Архитектура

### Текущая реализация: TUI (Terminal User Interface)

Приложение использует современный терминальный интерфейс на базе фреймворка **Textual**:
- Интерактивные экраны с навигацией по табам
- Виджеты для отображения статистики в реальном времени
- Встроенная панель логирования с цветовой дифференциацией уровней
- Асинхронная загрузка данных без блокировки интерфейса

**Структура TUI:**
- `HomeView` — главная панель со счетчиками ячеек, батарей, последней записью и логами
- `DataView` — просмотр и управление данными
- `SettingsView` — настройки приложения

### Планируемая реализация: Web API + Frontend

В будущем предусмотрена миграция на веб-интерфейс:
- **Backend**: FastAPI REST API
- **Frontend**: Веб-клиент для работы в браузере
- Сохранение текущей бизнес-логики и структуры данных

## Технологии

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white)
![Textual](https://img.shields.io/badge/Textual-000000?style=flat&logo=python&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=flat&logo=sqlalchemy&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat&logo=sqlite&logoColor=white)
![Pydantic](https://img.shields.io/badge/Pydantic-E92063?style=flat&logo=python&logoColor=white)
![Alembic](https://img.shields.io/badge/Alembic-CCCCFF?style=flat&logo=python&logoColor=black)

- **Python 3.12+**
- **Textual** — TUI фреймворк
- **SQLAlchemy 2.x** — ORM для работы с базой данных
- **Alembic** — миграции базы данных
- **Pydantic** — валидация данных и настройки
- **SQLite + aiosqlite** — асинхронная работа с БД

## Структура проекта

```
├── app/
│   ├── core/           # Конфигурация, логгер, база данных
│   ├── models/         # SQLAlchemy модели (Cell, Battery, ProductModel)
│   ├── repositories/   # Слой доступа к данным
│   ├── services/       # Бизнес-логика
│   ├── tui/            # Terminal UI компоненты
│   │   ├── views/      # Экраны приложения
│   │   └── widgets/    # Кастомные виджеты
│   ├── main.py         # Точка входа TUI приложения
│   └── messages.py     # Сообщения для коммуникации виджетов
├── alembic/            # Миграции базы данных
├── pyproject.toml      # Зависимости и метаданные проекта
└── poetry.lock         # Заблокированные версии зависимостей
```

## Установка и запуск

### Требования
- Python 3.12 или выше
- Poetry (менеджер зависимостей)

### Установка зависимостей

```bash
poetry install
```

### Инициализация базы данных

```bash
# Применение миграций
alembic upgrade head
```

### Запуск приложения

```bash
poetry run python -m app.main
```

## Модели данных

### Cell (Ячейка)
- `barcode` — уникальный штрих-код
- `capacity` — емкость
- `time_charged` / `time_discharged` — время заряда/разряда
- `tested_at` — дата тестирования
- Связи: `ProductModel`, `Battery`

### Battery (Батарея)
- Аналогичная структура с возможностью группировки ячеек

### ProductModel (Модель изделия)
- `number` — номер модели
- `type` — тип (battery/cell)
- Технические характеристики: напряжение, емкость, габариты, вес

## Интеграция с Neware

Приложение предназначено для работы с оборудованием Neware для тестирования аккумуляторов. Интеграция позволяет:
- Автоматически импортировать результаты тестов
- Отслеживать статус оборудования(в будущем)
- Формировать отчеты по циклам заряда-разряда

## Лицензия

MIT License

## Автор

- danilov-dev <dan.forth.ant@gmail.com>
