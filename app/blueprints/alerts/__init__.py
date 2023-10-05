from flask import Blueprint

alerts = Blueprint('alerts', __name__, template_folder='alerts_template', url_prefix='/alerts')

from . import routes