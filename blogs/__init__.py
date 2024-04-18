from flask import Blueprint


blogs_bp = Blueprint("blogs", __name__, template_folder="templates", url_prefix="/blogs")

from blogs import routes