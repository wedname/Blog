"""
Задание #1:
Нужно создать класс Users с полями:
 - id (Должен автоматически заполняться для каждого нового пользователя)
 - Имя
 - Почта
 - Телефон
 - Пароль
 - Повторение пароля
 - Аватарка
Добавить валидацию на поля:
 - Сложность пароля (Пароль должен быть больше 8 символов, 1 меленькая и большая буква, 1 цифра и спец. символ)
 - Повторение пароля (Подтверждение пароля должен совпадать с паролем)
 - В почте есть символы '@' и '.'
 - Аватарка формата '.jpg', для получения названия файла можно использовать 'request.files['название_поля'].filename
Реализовать функционал: добавления, удаления, изменения пользователя через класс
Создать функцию validate, которая возвращает True если валидация пройдена, иначе False
Создать функцию save, которая принимает в качестве аргумента - название файла и сохраняет все данные пользователей в
файл
Создать функцию load, которая принимает в качестве аргумента - название файла и загружает все данные пользователей из
файла
Задание 2:
Создать класс Articles с полями:
    author
    views_count
    img
    title
    text
Добавить валидацию:
    - Имя автора больше 2 символов
    - заголовок больше 1 символа и меньше 40 символов
    - текст больше 1 символа
Реализовать функционал: добавления, удаления, изменения данных через класс
Создать функцию validate, которая возвращает True если валидация пройдена, иначе False
Создать функцию save, которая принимает в качестве аргумента - название файла и сохраняет все данные в файл
Создать функцию load, которая принимает в качестве аргумента - название файла и загружает все данные из файла
"""

from flask import Flask, render_template, request, abort, redirect
import random
import string
import os
from blog import *

app = Flask(__name__)

blog = Blog()
articles = blog.posts_list
blog.add_post(
    'wedname',
    'First post',
    'Hello, guys! It`s my first website with backend! '
    'So, jwhnegipuw hriugropwijfvoiwejpfovj ewpofjerowjfoejfo ijweofjowe '
    'jgowejroi ugfwoief jowejfoi; jwefoijwe ofjowejf'
)


@app.route('/')
def main_page():
    return render_template('index.html', articles=articles)


@app.route('/generic')
def generic_page():
    return render_template('generic.html')


@app.route('/article/<int:id>')
def get_article(id):
    for article in articles:
        if article.id == id:
            article.views_count += 1
            return render_template('generic.html', article=article)
    abort(404)


@app.route('/create/article', methods=['GET', 'POST'])
def create_article():
    """
    Request methods:
        1) GET - Отвечает за получение данных
        2) POST - Отвечает за создание данных
        3) PUT - Отвечает за обновление данных
        4) DELETE - Отвечает за удаление данных
    """
    if request.method == 'GET':
        return render_template('create_article.html')
    elif request.method == 'POST':
        # image = request.files['article_image']
        # random_name = ''.join([random.choice(string.digits + string.ascii_letters) for x in range(10)])
        # img_path = f'static/images/{random_name}.jpg'
        # image.save(img_path)
        blog.add_post(
            author=request.form['article_author'],
            value_name=request.form['article_title'],
            value_description=request.form['article_text']
        )
        return redirect('/')
    else:
        return 'METHOD NOT ALLOWED'


if __name__ == '__main__':
    app.run(host='localhost', port=8000)
