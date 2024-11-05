from flask import render_template, request, url_for, redirect, make_response, session, flash
from datetime import timedelta, datetime
from . import  users_bp

@users_bp.route("/profile")
def get_profile():
    if "username" in session:
        username_value = session["username"]
        return render_template("profile.html", username=username_value)
    flash("Invalid: session", "danger")
    return redirect(url_for("user_name.login"))

@users_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("login") 
        session["username"]=username
        flash("Success: session added successfuly", "success")
        return redirect(url_for("user_name.get_profile"))
    return render_template("login.html")
 
@users_bp.route("/logout")
def logout():
    session.pop('username', None)
    session.pop('age', None)
    return redirect(url_for('user_name.get_profile'))
  
@users_bp.route("/<string:name>")
def greetings(name):
    name= name.upper()
    age = request.args.get("age", 0, int) # за завмовчуванням якщо вік не введений то 0, get по ключу витягує, args — словник

    return render_template("hi.html", name=name, age=age)

@users_bp.route("/")
def admin():
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