from flask import Flask, request, redirect, url_for

app=Flask(__name__)
app.config.from_pyfile("config.py") #словник
@app.route('/')
def main():
    return '<h1>Hello, world</h1>', 200

@app.route('/homepage') 
def home():
    """View for the Home page of your website."""
    agent=request.user_agent
    return f"This is your homepage :) - {agent} "

@app.route("/hi/<string:name>")
def greetings(name):
    name= name.upper()
    age = request.args.get("age", 0, int) # за завмовчуванням якщо вік не введений то 0, get по ключу витягує, args — словник
    year=2024-age
    return f"Welcome, {name} - {year}"

@app.route("/admin")
def admin():
   # to_url="/hi/administrator?age=45"
    to_url=url_for("greetings", name="administrator", age=45, external=True) #external абсолютний шлях
    return redirect(to_url)
if __name__=='__main__':
    app.run()