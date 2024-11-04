from flask import render_template, request, url_for, redirect, make_response
from datetime import timedelta, datetime
from . import  users_bp

@users_bp.route("/<string:name>")
def greetings(name):
    name= name.upper()
    age = request.args.get("age", 0, int) # за завмовчуванням якщо вік не введений то 0, get по ключу витягує, args — словник

    return render_template("hi.html", name=name, age=age)

@users_bp.route("/")
def admin():
   # to_url="/hi/administrator?age=45"
    to_url=url_for("users.greetings", name="administrator", age=45, external=True) #external абсолютний шлях
    return redirect(to_url)

@users_bp.route('/set_cookie')
def set_cookie():
    response = make_response('Кука встановлена')
    response.set_cookie('username', 'student', max_age=timedelta(seconds=60))
    response.set_cookie('color', '', max_age=timedelta(seconds=60))
    return response

@users_bp.route('/get_cookie')
def get_cookie():
    username = request.cookies.get('username')
    return f'Користувач: {username}'

@users_bp.route('/delete_cookie')
def delete_cookie():
    response = make_response('Кука видалена')
    response.set_cookie('username', '', expires=0) # response.set_cookie('username', '', max_age=0)
    return response