from flask import Blueprint

users_bp=Blueprint("user_name", __name__, url_prefix="/users", template_folder='templates/users',  static_folder='static', static_url_path="static_for_users")
from . import view
