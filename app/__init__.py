from flask import Flask
from pycoingecko import CoinGeckoAPI
from config import Config
from flask_login import LoginManager
from flask_migrate import Migrate
from .models import db, User


app = Flask(__name__)
cg = CoinGeckoAPI()

app.config.from_object(Config)

login_manager = LoginManager()

db.init_app(app)
migrate = Migrate(app,db)
login_manager.init_app(app)

login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'danger'

from app.blueprints.auth import auth
from app.blueprints.main import main
from app.blueprints.alerts import alerts
from app.blueprints.lists import lists

app.register_blueprint(auth)
app.register_blueprint(main)
app.register_blueprint(alerts)
app.register_blueprint(lists)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
    
    

from . import models