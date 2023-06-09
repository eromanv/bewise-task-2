# Bewise Task 2

Это пример приложения Bewise Music для создания пользователей и добавления аудиозаписей.

## Установка и запуск

1. Установите зависимости:

`pip install -r requirements.txt`

2. Примените миграции базы данных:

`python manage.py migrate`

3. Запустите сервер разработки Django:

`python manage.py runserver`

Приложение будет доступно по адресу `http://localhost:8000/`.

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
