from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
migrate = Migrate()

def create_app(config_name="config"):
    app=Flask(__name__)
    
    app.config.from_object("config")
    db.init_app(app)
    migrate.init_app(app, db)
    with app.app_context():
        from . import view
        from app.users.models import User
        from app.posts import post_bp 
        app.register_blueprint(post_bp)

        from app.users import users_bp 

        app.register_blueprint(users_bp, url_prefix="/users")
    return app
