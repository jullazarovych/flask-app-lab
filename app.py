from flask import Flask, request, redirect, url_for, render_template, abort

app=Flask(__name__)
app.config.from_pyfile("config.py") #словник
@app.route('/')
def main():
    return render_template("hello.html")

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

@app.route("/admin")
def admin():
   # to_url="/hi/administrator?age=45"
    to_url=url_for("greetings", name="administrator", age=45, external=True) #external абсолютний шлях
    return redirect(to_url)

posts = [
    {"id": 1, 'title': 'My First Post', 'content': 'This is the content of my first post.', 'author': 'John Doe'},
    {"id": 2, 'title': 'Another Day', 'content': 'Today I learned about Flask macros.', 'author': 'Jane Smith'},
    {"id": 3, 'title': 'Flask and Jinja2', 'content': 'Jinja2 is powerful for templating.', 'author': 'Mike Lee'}
]

@app.route('/posts')
def get_posts():
    return render_template("posts.html", posts=posts)

@app.route('/post/<int:id>')
def deatil_post(id):
    if id > 3:
        abort(404)
    post=posts[id-1]
    return render_template("detail_post.html", post=post)

if __name__=='__main__':
    app.run()