from flask import Blueprint

controllers = Blueprint("controllers", __name__, url_prefix="/api")

from .common import *
from .data import *
from .export import *
from .home_page import *
from .init import *
from .label import *
from .log import *
from .login import *
from .notice import *
from .preprocess import *
from .public import *
from .role import *
from .system import *
from .user import *
