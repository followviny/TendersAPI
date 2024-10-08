# API for tender management

## Требования

- Python 3.8+
- Docker (optional)

## Установка и настройка

1. Клонируйте репозиторий 
2. Создайте виртуальное окружение и активируйте его:
```
python3 -m venv .env
source .env/bin/activate
```
3. Установите зависимости:
```
pip install -r requirements.txt
```

## Создание базы данных
1. После запуска PostgreSQL используйте следующие команды SQL для создания необходимых таблиц:
```
CREATE TABLE employee (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    username VARCHAR(50) UNIQUE NOT NULL,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TYPE organization_type AS ENUM (
    'IE',
    'LLC',
    'JSC'
);

CREATE TABLE organization (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL,
    description TEXT,
    type organization_type,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE organization_responsible (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    organization_id UUID REFERENCES organization(id) ON DELETE CASCADE,
    user_id UUID REFERENCES employee(id) ON DELETE CASCADE
);

```
2. Добавьте данные сотрудников и их организаций в эти таблицы, чтобы программа могла с ними работать.
3. Настройте переменные окружения в database.py

## Проверка работоспособности

Запустите main.py

После запуска приложение будет доступно по адресу: http://localhost:8080

Для проверки API вы можете использовать Swagger UI, доступный по адресу: http://localhost:8080/docs

## Запуск через Docker
1. Убедитесь, что у вас установлен Docker.

2. Клонируйте репозиторий
3. Соберите Docker образ
```
docker build -t pythonprojectavito .
```
Запустите контейнер:
```
docker run -p 8080:8080 pythonprojectavito
```
# Детали реализации API и бизнес-логика

## Тендеры
Создаются только ответственными за организацию от ее имени

Создание:
 - Тендер создан - статус CREATED (Доступен только ответственым за организацию)
 - Публикация: - статус PUBLISHED (Доступен любому)
 - Закрытие: - статус CLOSED (Доступен только ответственным за организацию)

Редактирование:
 - Увеличивается версия

## Предложения
Один пользователь может быть ответственным в одной организации
->
Создаются пользователями, которые ответственны за какую-либо организацию. Они могут выбрать тип автора, как себя или организацию, но id должны указывать свой

 - Предложение создано - статус CREATED (Доступно только автору)
 - Публикация: - статус PUBLISHED (Доступно автору и ответственным со стороны тендера)
 - Закрытие: - статус CANCELED (Доступно только автору)

Редактирование:
 - Увеличивается версия

## Статусы
 - Изменяются отдельным запросом, версия при этом не увеличивается


## Согласование/отклонение

Доступно только ответственным за организацию, связанной с тендером

Расширенный процесс согласования:
- Если есть хотя бы одно решение reject, предложение отклоняется
- Для согласования предложения нужно получить решения больше или равно кворуму
- Кворум = min(3, количество ответственных за организацию)

## Просмотр отзывов на прошлые предложения
- Ответственный за организацию может просмотреть отзывы на предложения автора, который создал предложение для его тендера
## Оставление отзывов на предложение
- Ответственный за организацию может оставить отзыв на предложение
## Откат
- После отката, считается новой правкой с увеличением версии
(Статус не может изменяться)
