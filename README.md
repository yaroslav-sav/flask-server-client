# Гостевая книга v3

Flask-приложение для заметок с авторами и лайками.

## Хранение

Все заметки лежат в notes.json. Файл перезаписывается при каждом добавлении, редактировании, удалении и лайке.

## Эндпоинты

- GET /notes — список (фильтр author, пагинация limit/offset, сортировка sort/order)
- POST /notes — создать (text, author)
- GET /notes/<id> — получить
- PUT /notes/<id> — заменить (text, author)
- PATCH /notes/<id> — обновить text
- DELETE /notes/<id> — удалить
- DELETE /notes?author=<имя> — удалить все заметки автора
- POST /notes/<id>/like — лайк
- GET /authors — статистика по авторам

## Запуск

Сервер: http://127.0.0.1:5000
