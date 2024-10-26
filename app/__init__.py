from flask import Flask

app=Flask(__name__)
app.config.from_pyfile("../config.py")

from . import view
from app.posts import post_bp 
app.register_blueprint(post_bp)
