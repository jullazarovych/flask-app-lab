from flask import render_template, request, url_for, redirect, make_response, session, flash
from datetime import timedelta, datetime
from flask import current_app
from app import login_manager
from flask_login import login_user, logout_user, current_user, login_required
from . import  users_bp
from app.users.forms import RegistrationForm, UpdateAccountForm
from app.users.models import User, LoginForm
from app import db
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash
from PIL import Image
import os

VALID_USERNAME = "student"
VALID_PASSWORD = "12345678"

@users_bp.route('/resume')
def resume():
    return render_template('resume.html', title="Резюме ")

@users_bp.route("/profile")
@login_required
def get_profile():
    cookies = request.cookies.to_dict()
    theme = request.cookies.get("theme", "light")
    return render_template("profile.html", username=current_user.username, cookies=cookies, theme=theme)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@users_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()  
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            login_user(user, remember=form.remember.data) 
            flash('Login successful!', 'success')
            return redirect(url_for('user_name.account')) 
        else:
            flash('Invalid credentials.', 'danger')

    return render_template('login.html', form=form)

from PIL import Image
import os
from werkzeug.utils import secure_filename

def save_picture(form_picture):
    try:
        filename = secure_filename(form_picture.filename)
        picture_folder = os.path.join(users_bp.static_folder, 'profile_pics')
        if not os.path.exists(picture_folder):
            os.makedirs(picture_folder)

        picture_path = os.path.join(picture_folder, filename)

        image = Image.open(form_picture)

        min_side = min(image.size)  
        left = (image.width - min_side) / 2
        top = (image.height - min_side) / 2
        right = (image.width + min_side) / 2
        bottom = (image.height + min_side) / 2

        image = image.crop((left, top, right, bottom))
        output_size = (150, 150)
        image.thumbnail(output_size)
        image.save(picture_path)

        return filename
    except Exception as e:
        return None


@users_bp.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm(username=current_user.username, email=current_user.email, about_me=current_user.about_me)
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            if picture_file:
                current_user.image_file = picture_file
            else:
                flash("Failed to save picture")

        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.about_me = form.about_me.data
        if form.password.data:
            current_user.set_password(form.password.data)
            flash('Your password has been updated!', 'success')

        db.session.commit()
        flash('Your account has been updated!', 'success')
        
        return redirect(url_for('user_name.account'))
    elif (form.validate_on_submit()!=True):
        for field, errors in form.errors.items():
            for error in errors:
                flash(f"Error in {field}: {error}", 'danger')
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_path = os.path.join(users_bp.static_folder, 'profile_pics', current_user.image_file)
    if current_user.image_file and os.path.isfile(image_path):
        image_file = url_for('user_name.static', filename='profile_pics/' + current_user.image_file)
    else:
        image_file = url_for('user_name.static', filename='profile_pics/profile_default.jpg')
    return render_template("account.html", username=current_user.username, email=current_user.email, image_file=image_file, form=form)

@users_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data, image_file='profile_default.jpg')
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created!', 'success')
        return redirect(url_for('user_name.register'))
    return render_template('register.html', form=form)

@users_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have successfully logged out", "success")
    return redirect(url_for('user_name.login'))

@users_bp.route("/set_theme/<theme>")
def set_theme(theme):
    if theme not in ["light", "dark"]:
        flash("Invalid theme selected.", "danger")
        return redirect(url_for("user_name.get_profile"))

    response = make_response(redirect(url_for("user_name.get_profile")))
    response.set_cookie("theme", theme, max_age=3600*24)  
    flash(f"Theme set to {theme}.", "success")
    return response


@users_bp.route("/<string:name>")
def greetings(name):
    name= name.upper()
    age = request.args.get("age", 0, int) 

    return render_template("hi.html", name=name, age=age)

@users_bp.route("/users")
@login_required
def user_list():
    users = User.query.all()  
    user_count = len(users)   
    return render_template("user_list.html", users=users, user_count=user_count)

@users_bp.route("/")
def admin():
    to_url = url_for("user_name.greetings", name="administrator", age=45, _external=True)  # змінено на "user_name.greetings"
    return redirect(to_url)

@users_bp.route('/set_cookie', methods=["POST"])
@login_required
def set_cookie():
    key = request.form.get("key")
    value = request.form.get("value")
    expiry = int(request.form.get("expiry"))

    response = make_response(redirect(url_for("users_bp.get_profile")))
    response.set_cookie(key, value, max_age=expiry)
    flash(f"Cookie '{key}' added successfully", "success")
    return response


@users_bp.route('/get_cookie')
def get_cookie():
    username = request.cookies.get('username')
    return f'User: {username}'

@users_bp.route('/delete_cookie', methods=["POST"])
@login_required
def delete_cookie():
    key = request.form.get("key")
    response = make_response(redirect(url_for("users_bp.get_profile")))

    if key:
        response.set_cookie(key, '', expires=0)
        flash(f"Cookie '{key}' deleted successfully", "success")
    else:
        for key in request.cookies:
            response.set_cookie(key, '', expires=0)
        flash("All cookies deleted successfully", "success")

    return response
