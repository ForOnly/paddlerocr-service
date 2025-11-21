# @description: 
# @author: licanglong
# @date: 2025/11/20 14:21
from flask import Blueprint

base_bp = Blueprint("base", __name__, url_prefix='/')

from app.blueprints.base import routes  # noqa
