# Bewise Task 2

Это приложение Bewise Radio/Music для создания пользователей и добавления аудиозаписей, и дальнейшего их скачивания

## Технологии

Django REST Framework, PostgreSQL, Docker

## Покрытие тестами

Для запуска pytest выполните команду:

`docker-compose exec web pytest`

## Установка и запуск

1. Установите Docker, если его еще нет на вашей системе.

2. Клонируйте репозиторий Radio на свою локальную машину:

  `git clone https://github.com/eromanv/bewise-task-2.git`

3. Перейдите в каталог infra:

    `cd infra`

4. Создайте файл .env

        DB_ENGINE=django.db.backends.postgresql
        DB_NAME=postgres
        POSTGRES_USER=postgres
        POSTGRES_PASSWORD=postgres
        DB_HOST=db
        DB_PORT=5432

5. Запустите контейнеры Docker с помощью docker-compose:

`docker-compose up -d`

## REST API

### Создание пользователя

**URL:** `/api/create_user/`

**Метод:** POST

**Параметры запроса:**

| Параметр | Тип данных | Описание     |
|----------|------------|--------------|
| name     | Строка     | Имя пользователя |

**Пример запроса:**

`curl -X POST -H "Content-Type: application/json" -d '{"name": "John"}' http://localhost:8000/api/create_user/`

**Пример ответа:**

`
{
  "user_id": "e1c2e690-866e-4f2a-aedc-64c9c84a1475",
  "access_token": "2b7039e8-6f8b-4a4c-ba24-843bae39e0e6"
}
`

### Добавление аудиозаписи

**URL:** `/api/add_audio/`

**Метод:** POST

**Параметры запроса:**

| Параметр   | Тип данных |  Описание                  |
|------------|------------|----------------------------|
| user_id    | Строка     | Идентификатор пользователя |
|access_token| Строка     | Токен доступа пользователя |
|audio_file  | Файл       | Аудиозапись в формате WAV  |

**Пример запроса:**

`curl -X POST -H "Content-Type: multipart/form-data" -F "user_id=e1c2e690-866e-4f2a-aedc-64c9c84a1475" -F "access_token=2b7039e8-6f8b-4a4c-ba24-843bae39e0e6" -F "audio_file=@audio.wav" <http://localhost:8000/api/add_audio/>`

**Пример ответа:**

`{
  "download_url": "<http://localhost:8000/record?id=3e5c79e0-75e1-4c4d-b79c-3a1ccbb07e56&user=e1c2e690-866e-4f2a-aedc-64c9c84a1475>"
}`

### Доступ к аудиозаписи

**URL:** `/record/`

**Метод:** GET

**Параметры запроса:**

| Параметр   | Тип данных |  Описание                  |
|------------|------------|----------------------------|
| id         | Строка     |  Идентификатор аудиозаписи |
|user        | Строка     | Идентификатор пользователя |

**Пример запроса:**

`<http://localhost:8000/record?id=3e5c79e0-75e1-4c4d-b79c-3a1ccbb07e56&user=e1c2e690-866e-4f2a-aedc-64c9c84a1475>`

**Пример ответа:**

Аудиозапись будет скачана с использованием HTTP.

## Автор

Егоров Роман (@eromanvad)