# Foodgram - продуктовый помощник
Дипломный проект Яндекс.Практикум факультет backend-разработки
## Описание проекта
<b>Foodgram</b> - сервис, на котором пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.
## Стек
* [Django==4.1.6](https://www.djangoproject.com/)
* [djangorestframework==3.14.0](https://www.django-rest-framework.org/)
* [PyJWT==2.6.0](https://pyjwt.readthedocs.io/en/stable/)
* [gunicorn==20.1.0](https://gunicorn.org/)
* [Docker](https://docs.docker.com/)
* [NGINX](https://nginx.org/ru/)
* [POSTGRES](https://www.postgresql.org/)
## Как развернуть проект на удаленном сервере
Клонировать репозиторий и перейти в него в командной строке:
```
git clone git@github.com:MrSlavencio/foodgram-project-react.git
```
В директории *infra* создать файл *.env*:
```
cd infra
nano .env
```
Заполнить файл *.env* переменными окружения:
```
DB_ENGINE=django.db.backends.postgresql
DB=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=<Ваш пароль от БД>
DB_HOST=db
DB_PORT=5432
```
Из директории *infra* по очереди выполнить команды:
```
sudo docker-compose up -d
sudo docker-compose exec web python manage.py migrate
sudo docker-compose exec web python manage.py createsuperuser
sudo docker-compose exec web python manage.py collectstatic --no-input
```
<b>Контейнер запущен на `http://84.252.138.45/` и 'http://foodgram-slava.hopto.org/'!</b></br>
Проверьте работу админ-панели, перейдя по [ссылке](http://foodgram-slava.hopto.org/admin/):
```
{
    "admin-login": "admin@admin.ru",
    "admin-pass": "foodgramDIPLOMA"
}
```
**Подключение к БД через pgAdmin**</br>
Регистрируем сервер</br>
На вкладке *Connection*:
* **Host name/adress** - внешний ip-адрес виртуальной машины
* **Port** - порт, на котором запущена postgre (указан в docker-compose)
* **Maintaince database** - название БД (из .env)
* **Username** - пользователь БД (из .env или другой, если другой юзер создан)
* **Password** - пароль пользователя от БД (из .env или другой, если другой юзер создан)
## Примеры API-запросов
**Регистрация пользователей**
```
POST http://<host>/api/users/
{
    "email": "vpupkin@yandex.ru",
    "username": "vasya.pupkin",
    "first_name": "Vasya",
    "last_name": "Pupkin",
    "password": "Qwgja2f12pz3"
}
```
**Авторизация пользователя (получение токена)**
```
POST http://<host>/api/auth/token/login/
{
    "password": "string",
    "email": "string"
}
```
**Удаление токена**
```
Authorization: Token <USER'S TOKEN>
POST http://<host>/api/auth/token/logout/
```
**Смена пароля**
```
POST http://<host>/api/users/set_password/
Authorization: Token <USER'S TOKEN>
{
    "new_password": "string",
    "current_password": "string"
}
```
**Получение информации о текущем пользователе**
```
GET http://<host>/api/users/me/
```
**Получение информации о пользователе по его id**
```
GET http://<host>/api/users/{id}/
```
**Получение информации о всех пользователях**
```
GET http://<host>/api/users/
```
**Получение списка подписок**
```
Authorization: Token <USER'S TOKEN>

Параметры запроса:
- page (integer) — номер страницы
- limit (integer) — количество подписок в выдаче
- recipes_limit (integer) — максимальное количество рецептов пользователя в выдаче

GET http://<host>/api/users/subscriptions/
```
**Подписаться на пользователя**
```
Authorization: Token <USER'S TOKEN>

Параметры запроса:
- recipes_limit (integer) — максимальное количество рецептов пользователя в выдаче

POST http://<host>/api/users/{id}/subscribe/
```
**Отписаться от пользователя**
```
Authorization: Token <USER'S TOKEN>

DELETE http://<host>/api/users/{id}/subscribe/
```
**Получить список тегов**
```
GET http://<host>/api/tags/
```
**Получить тег по id**
```
GET http://<host>/api/tags/{id}/
```
**Получить список ингредиентов**
```
Параметры запроса:
- name (string) — поиск ингредеиента по части его названия (с начала строки)

GET http://<host>/api/ingredients/
```
**Получить ингредиент по id**
```
GET http://<host>/api/ingredients/{id}/
```
**Получить рецепты**
```
Параметры запроса:
- page (integer) — номер страницы
- limit (integer) — количество рецептов на странице
- is_favorited (integer 0 или 1) — фильтрация, добавлен ли рецепт в избранное
- is_in_shopping_cart (integer 0 или 1) — фильтрация, добавлен ли рецепт в список покупок
- author (integer) — фильтрация по id автора рецепта
- tags (slug) — фильтрация по тегу, допустим выбор нескольких тегов (?tags=breakfast&tags=dinner)

GET http://<host>/api/recipes/
```
**Получить рецепт по id**
```
GET http://<host>/api/recipes/{id}/
```
**Создать рецепт**
```
Authorization: Token <USER'S TOKEN>

POST http://<host>/api/recipes/
{
    "ingredients": [
        {
            "id": 3,
            "amount": 300
        }
    ],
    "tags": [
        1,
        2
    ],
    "image": "base64 encoded image",
    "name": "string",
    "text": "string",
    "cooking_time": 1
}
```
**Редактировать рецепт**
```
Authorization: Token <USER'S TOKEN>
*Доступно только автору рецепта

PATCH http://<host>/api/recipes/{id}/
{
    "ingredients": [
        {
            "id": 3,
            "amount": 500
        }
    ],
    "tags": [
        1
    ],
}
```
**Удаление рецепта**
```
Authorization: Token <USER'S TOKEN>
*Доступно только автору рецепта

DELETE http://<host>/api/recipes/{id}/
```
**Добавить рецепт в избранное**
```
Authorization: Token <USER'S TOKEN>

POST http://<host>/api/recipes/{id}/favorite/
```
**Удаление рецепта из избранного**
```
Authorization: Token <USER'S TOKEN>

DELETE http://<host>/api/recipes/{id}/favorite/
```
**Добавить рецепт в список покупок**
```
Authorization: Token <USER'S TOKEN>

POST http://<host>/api/recipes/{id}/shopping_cart/
```
**Удалить рецепт из списка покупок**
```
Authorization: Token <USER'S TOKEN>

DELETE http://<host>/api/recipes/{id}/shopping_cart/
```
**Скачать список покупок**
```
Authorization: Token <USER'S TOKEN>

GET http://<host>/api/recipes/download_shopping_cart/
```
Полная документация REST-API с ответами сервера доступна в файле `docs\openapi-schema.yml`.
## Об авторе
Автор проекта - **Кобзев Вячеслав**, студент когорты 44 факультета Бэкенд разработки Яндекс-практикума.</br>
Контакты для связи: </br>
[*telegram*](https://t.me/mrslavencio "MrSlavencio")

