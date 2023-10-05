from flask import Blueprint

lists = Blueprint('lists', __name__, template_folder='list_templates', url_prefix='/lists')

from . import routes