from flask import Flask
def create_app(config_name="config"):
    app=Flask(__name__)
    #app.config.from_pyfile("../config.py")
    app.config.from_object("config")
    with app.app_context():
        from . import view

        from app.posts import post_bp 
        app.register_blueprint(post_bp)

        from app.users import users_bp 

        app.register_blueprint(users_bp, url_prefix="/users")
        
    return app
