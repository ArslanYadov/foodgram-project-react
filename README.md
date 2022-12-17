# Foodgram 
[![Build Status](https://github.com/ArslanYadov/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)](https://github.com/ArslanYadov/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)

### Request
``` bash
$ curl http://localhost:8000/api/recipes/
```
### Response
``` bash
{
    "count": 1,
    "next": null,
    "previous": null,
    "results":  [
        {
            "id": 1,
            "tags": [
                {
                    "id": 2,
                    "name": "Обед",
                    "color": "#49B64E",
                    "slug": "lunch"
                }
            ],
            "author": {
                "email": "vpupkin@yandex.ru",
                "id": 1,
                "username": "vasya.pupkin",
                "first_name": "Вася",
                "last_name": "Пупкин",
                "is_subscribed": false
            },
            "ingredients": [
                {
                    "id": 1916,
                    "name": "фарш (свинина и курица)",
                    "measurement_unit": "г",
                    "amount": 500
                },
                {
                    "id": 886,
                    "name": "лук репчатый",
                    "measurement_unit": "г",
                    "amount": 100
                }
            ],
            "is_favorited": false,
            "is_in_shopping_cart": false,
            "name": "Котлета по киевски",
            "image": "http://localhost:8000/media/recipes/images/temp.png",
            "text": "Рецепт приготовления котлеты по киевски.",
            "cooking_time": 40
        }
    ]
}
```
### Описание

### Технологии
* Python 3.10.6
* Django 4.1.4 + REST
## Запуск проекта на данный момент
- В `settings.py` раскомментить нужную БД. (сейчас для дебага используется _sqlite_)
- Добавить в свой файл с переменными окружения `.env` значения переменных по примеру из файла `.env.template`
- Воспользоваться командой `make setup` из файла **Makefile** для сбора и запуска проекта на локальном сервере
``` bash
$ make setup
```
## Автор бэкенда
Арслан Ядов

E-mail:
[Arslan Yadov](mailto:arslanyadov@yandex.ru?subject=foodgram%20diplom%20project)
