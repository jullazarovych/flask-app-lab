from flask import render_template, abort, flash,redirect, url_for, session
from . import  post_bp
from .forms import PostForm
import json
from .utils import load_posts, save_post, get_post
import os
from .models import Post, Tag
from app.users.models import User
from app import db
from datetime import datetime as dt, date, datetime

@post_bp.route('/add', methods=['GET', 'POST'])
def add_post():
    form = PostForm()


    authors = User.query.all()
    form.author_id.choices = [(author.id, author.username) for author in authors]

    tags = Tag.query.all()
    form.tags.choices = [(tag.id, tag.name) for tag in tags]
    
    if form.validate_on_submit():
        if isinstance(form.publish_date.data, (datetime, date)):
            publish_date_str = form.publish_date.data.strftime('%Y-%m-%dT%H:%M')
            posted_date = datetime.strptime(publish_date_str, '%Y-%m-%dT%H:%M')
        else:
            posted_date = datetime.strptime(form.publish_date.data, '%Y-%m-%dT%H:%M')

        new_post = Post(
            title=form.title.data,
            content=form.content.data,
            is_active=form.is_active.data,
             posted=posted_date,  
            category=form.category.data,
            user_id=form.author_id.data
        )
        for tag_id in form.tags.data:
            tag = Tag.query.get(tag_id)
            if tag:
                new_post.tags.append(tag)
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
    post = db.get_or_404(Post, id)
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
