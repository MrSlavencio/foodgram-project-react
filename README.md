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
