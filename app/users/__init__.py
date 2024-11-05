from flask import Blueprint

users_bp=Blueprint("user_name", __name__, url_prefix="/users", template_folder='templates/users')
from . import view
