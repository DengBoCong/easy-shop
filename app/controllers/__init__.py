from flask import Blueprint

controllers = Blueprint("controllers", __name__, url_prefix="/api")

from .area import *
from .color import *
from .common import *
from .good import *
from .login import *
from .order import *
from .system import *
from .user import *
