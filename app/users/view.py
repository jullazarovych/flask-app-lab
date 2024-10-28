from flask import render_template, request, url_for, redirect
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
