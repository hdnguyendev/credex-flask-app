from flask import Blueprint

bp = Blueprint('accounts', __name__)

from . import routes 