from flask import Blueprint

announce_bp=Blueprint("announce", __name__, url_prefix="/announcements", template_folder='templates/announcements',  static_folder='static', static_url_path="static_for_announcements")
from . import view
