from flask import  request, redirect, url_for, render_template, abort
from . import app
@app.route('/')
def main():
    return render_template("base.html")

@app.route('/homepage') 
def home():
    """View for the Home page of your website."""
    agent=request.user_agent                        #контекст
    return render_template("home.html", agent=agent) # зліва змінна в шаблоні, справа її значення 

@app.route("/hi/<string:name>")
def greetings(name):
    name= name.upper()
    age = request.args.get("age", 0, int) # за завмовчуванням якщо вік не введений то 0, get по ключу витягує, args — словник

    return render_template("hi.html", name=name, age=age)
#admin
@app.route("/admin")
def admin():
   # to_url="/hi/administrator?age=45"
    to_url=url_for("greetings", name="administrator", age=45, external=True) #external абсолютний шлях
    return redirect(to_url)

#posts

@app.route('/resume')
def resume():
    return render_template('resume.html', title="Резюме ")
