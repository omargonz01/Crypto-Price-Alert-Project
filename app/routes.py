from flask import  request, render_template, flash, redirect, url_for 
import requests
from app import app, cg
from .blueprints.auth.forms import LoginForm, SignupForm 
from flask_login import login_user, logout_user, current_user, login_required
from .models import User, db
from werkzeug.security import check_password_hash


@app.route('/user/<string:name>')
@login_required
def users(name):
    return f'this is {name } page'

@app.route('/user/alerts')
@login_required
def alerts(alert_list):
    return f'this is {alert_list} page'



@app.route('/price/<coin>', methods=['GET', 'POST'])
def price(coin):
    data = cg.get_coin_by_id(id=coin)
    all_time_high = data['market_data']['ath']['usd']
    current_price = data['market_data']['current_price']['usd']
    return render_template('home.html', coin=coin, all_time_high=all_time_high, current_price=current_price)


# def index():
#     if request.method == 'POST':
#         coin = request.form.get('coin')
#         data = cg.get_coin_by_id(id=coin)
#         all_time_high = data['market_data']['ath']['usd']
#         current_price = data['market_data']['current_price']['usd']
#         return render_template('index.html', coin=coin, all_time_high=all_time_high, current_price=current_price)
#     return render_template('index.html')