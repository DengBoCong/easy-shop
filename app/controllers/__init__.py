from flask import Blueprint

controllers = Blueprint("controllers", __name__, url_prefix="/api")

from .login import *
from .user import *
