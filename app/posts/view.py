from flask import render_template, abort, flash,redirect, url_for, session
from . import  post_bp
from .forms import PostForm
import json
from .utils import load_posts, save_post, get_post
import os
from .models import Post
from app import db
from datetime import datetime as dt, date

@post_bp.route('/add', methods=['GET', 'POST'])
def add_post():
    form = PostForm()

    if form.validate_on_submit():
        new_post = Post(
            title=form.title.data,
            content=form.content.data,
            is_active=form.is_active.data,
            posted=dt.strptime(form.publish_date.data, '%Y-%m-%dT%H:%M'),  
            category=form.category.data
        )
        db.session.add(new_post)
        db.session.commit()
        flash(f"Post '{new_post.title}' added successfully!", "success")
        return redirect(url_for('posts.get_posts'))

    return render_template("add_post.html", form=form)
@post_bp.route('/')
def get_posts():
    stmt = db.select(Post).order_by(Post.posted.desc())
    posts = db.session.scalars(stmt).all()
    return render_template("posts.html", posts=posts)

@post_bp.route('/<int:id>')
def detail_post(id):
    stmt = db.select(Post)
    posts = db.session.scalars(stmt).all()
    total_posts = len(posts)
    if id > total_posts or id < 1:
        abort(404)
    post=posts[id-1]
    return render_template("detail_post.html", post=post)


@post_bp.route('/delete/<int:id>', methods=["POST"])
def delete_post(id):
    post = db.get_or_404(Post, id)
    
    db.session.delete(post)
    db.session.commit()

    flash(f"Post '{post.title}' has been deleted.", "success")
    return redirect(url_for('posts.get_posts'))

@post_bp.route('/edit/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    post = db.get_or_404(Post, post_id)
    form = PostForm(obj=post)


    if form.publish_date.data is None:
        form.publish_date.data = post.posted

    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.is_active = form.is_active.data

    
        if isinstance(form.publish_date.data, date):  
            post.posted = dt.combine(form.publish_date.data, dt.min.time())
        else:
            post.posted = form.publish_date.data

        post.category = form.category.data

        db.session.commit()
        flash(f"Post '{post.title}' updated successfully!", "success")
        return redirect(url_for('posts.get_posts'))

    return render_template("add_post.html", form=form)
