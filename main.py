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
from users import *

app = Flask(__name__)

ath_user = None
ath = False

blog = Blog()
articles = blog.posts_list

users = Users('./users.json')

blog.add_post(
    'wedname',
    'First post',
    'Hello, guys! It`s my first website with backend! '
    'So, jwhnegipuw hriugropwijfvoiwejpfovj ewpofjerowjfoejfo ijweofjowe '
    'jgowejroi ugfwoief jowejfoi; jwefoijwe ofjowejf',
    "test_tag first_post"
)

blog.add_post(
    'wedname',
    'Second post',
    'Hello, guys! It`s my first website with backend! '
    'So, jwhnegipuw hriugropwijfvoiwejpfovj ewpofjerowjfoejfo ijweofjowe '
    'jgowejroi ugfwoief jowejfoi; jwefoijwe ofjowejf',
    "test_tag second_post"
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
            value_description=request.form['article_text'],
            tags=request.form['article_tags']
        )
        return redirect('/')
    else:
        return 'METHOD NOT ALLOWED'


@app.route('/article/tag/<tag>', methods=['GET'])
def search_articles_by_tags(tag):
    articles_by_tag = []
    for article in articles:
        for j in range(len(article.tags)):
            if article.tags[j] == tag:
                articles_by_tag.append(article)
    return render_template('search_by_tags.html', articles_by_tag=articles_by_tag, articles=articles)


@app.route('/create/user', methods=['GET', 'POST'])
def create_user():
    if request.method == 'GET':
        return render_template('create_user.html')
    elif request.method == 'POST':
        # image = request.files['article_image']
        # random_name = ''.join([random.choice(string.digits + string.ascii_letters) for x in range(10)])
        # img_path = f'static/images/{random_name}.jpg'
        # image.save(img_path)
        if request.form['confirm_password'] == request.form['password']:
            users.create_user(
                name=request.form['username'],
                email=request.form['email'],
                password=request.form['password']
            )
            return redirect('/')
        else:
            return redirect('/create/user')
    else:
        return 'METHOD NOT ALLOWED'


@app.route('/authorization', methods=['GET', 'POST'])
def authorization():
    global ath_user
    global ath

    if request.method == 'GET':
        return render_template('authorization.html')
    elif request.method == 'POST':
        if users.search_user(request.form['email']) is not None:
            user = users.auth_user_id(request.form['email'])
            if request.form['password'] == users.users[user]['password']:
                ath_user = user
                ath = True
                print('Все норм!')
                return redirect(f'/user/{ath_user}')
            print('Не тот пароль!')
            return redirect('/authorization')
        else:
            return redirect('/create/user')
    else:
        return 'METHOD NOT ALLOWED'


@app.route('/users', methods=['GET'])
def get_users():
    return render_template('users.html', users=users.users)


@app.route('/user/<int:id>', methods=['GET'])
def get_user(id):
    for user in users.users:
        if user['id'] == id:
            return render_template('user.html', user=user)
    abort(418)


if __name__ == '__main__':
    app.run(host='localhost', port=8000)
