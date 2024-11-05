from flask import render_template, request, url_for, redirect, make_response, session, flash
from datetime import timedelta, datetime
from . import  users_bp

VALID_USERNAME = "student"
VALID_PASSWORD = "12345678"

@users_bp.route("/profile")
def get_profile():
    if "username" in session:
        username_value = session["username"]
        cookies = request.cookies.to_dict()  
        theme = request.cookies.get("theme", "light")  

        return render_template("profile.html", username=username_value, cookies=cookies)
    
    flash("Invalid: session", "danger")
    
    return redirect(url_for("user_name.login"))

@users_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username") 
        password = request.form.get("password")
        
        if username == VALID_USERNAME and password == VALID_PASSWORD:
            session["username"] = username  
            flash("Successfuly login!", "success")
            return redirect(url_for("user_name.get_profile"))
        else:
            flash("Unvalid username or password", "danger")
            return redirect(url_for("user_name.login"))

    return render_template("login.html")

@users_bp.route("/logout", methods=["GET", "POST"])
def logout():
    session.pop('username', None)
    session.pop('password', None)
    
    flash("You succesfully log out", "success")
    
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

@users_bp.route("/")
def admin():
    to_url = url_for("user_name.greetings", name="administrator", age=45, _external=True)  # змінено на "user_name.greetings"
    return redirect(to_url)





@users_bp.route('/set_cookie', methods=["POST"])
def set_cookie():
    if "username" not in session:
        flash("Please log in to manage cookies.", "danger")
        return redirect(url_for("user_name.login"))
    
    key = request.form.get("key")
    value = request.form.get("value")
    expiry = int(request.form.get("expiry"))
    
    response = make_response(redirect(url_for("user_name.get_profile")))
    response.set_cookie(key, value, max_age=expiry)
    flash(f"Cookie '{key}' added successfully", "success")
    return response

@users_bp.route('/get_cookie')
def get_cookie():
    username = request.cookies.get('username')
    return f'User: {username}'

@users_bp.route('/delete_cookie', methods=["POST"])
def delete_cookie():

    if "username" not in session:
        flash("Please log in to manage cookies", "danger")
        return redirect(url_for("user_name.login"))
    
    key = request.form.get("key")
    response = make_response(redirect(url_for("user_name.get_profile")))
    
    if key:
        response.set_cookie(key, '', expires=0)
        flash(f"Cookie '{key}' deleted successfully", "success")
    else:
        for key in request.cookies:
            response.set_cookie(key, '', expires=0)
        flash("All cookies deleted successfully", "success")
    
    return response