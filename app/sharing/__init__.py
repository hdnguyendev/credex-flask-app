from flask import Blueprint

bp = Blueprint('sharing', __name__)

from app.sharing import routes 