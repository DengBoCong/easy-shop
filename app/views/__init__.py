from flask import Blueprint

views = Blueprint("views", __name__, url_prefix="/")

from .admin import *
from .public import *
from .customer import *
