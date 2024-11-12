from flask import render_template, abort, flash,redirect, url_for, session
from . import  post_bp
from .forms import PostForm
import json
import os

POSTS_FILE = "posts.json"

def load_posts():
    if os.path.exists(POSTS_FILE):
        with open(POSTS_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    return []
def save_posts(posts):
    with open(POSTS_FILE, "w", encoding="utf-8") as file:
        json.dump(posts, file, ensure_ascii=False, indent=4)

@post_bp.route('/add_post', methods=["GET", "POST"])
def add_post():
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        is_active = form.is_active.data
        publish_date = form.publish_date.data.strftime('%Y-%m-%d')
        category = form.category.data
        #### 
        posts = load_posts()
        author = session.get('username', 'Anonymous')
        new_post = {
            "id": len(posts) + 1, 
            "title": title,
            "content": content,
            "author": author,
            "is_active": is_active,
            "publish_date": publish_date,
            "category": category
        }
        posts.append(new_post)
        save_posts(posts)
        flash(f"Post {title} added succesfully")
        return redirect(url_for(".get_posts"))
    
    return render_template("add_post.html", form=form)

@post_bp.route('/')
def get_posts():
    posts = load_posts()
    return render_template("posts.html", posts=posts)

@post_bp.route('/<int:id>')
def detail_post(id):
    posts = load_posts()
    total_posts = len(posts)
    if id > total_posts or id < 1:
        abort(404)
    post=posts[id-1]
    return render_template("detail_post.html", post=post)

