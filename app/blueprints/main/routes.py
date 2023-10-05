from app import app, cg
from . import main
from flask import render_template, request, flash, url_for, redirect
from flask_login import login_required, current_user


@main.route('/home')
@main.route('/')
def home():
    return render_template('home.html')

@main.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    if request.method == 'POST':
        coin = request.form.get('coin')

        # Check if the coin input is empty
        if not coin:
            flash('No search, no service. Don’t be shy... search any crypto!', 'danger')
            return redirect(url_for('main.search'))

        try:
            data = cg.get_coin_by_id(id=coin)
            all_time_high = data['market_data']['ath']['usd']
            current_price = data['market_data']['current_price']['usd']
            coin_symbol = data['symbol']
            market_cap = data['market_data']['market_cap']['usd']
        
            return render_template('search.html', coin=coin, all_time_high=all_time_high, current_price=current_price, 
            coin_symbol=coin_symbol, market_cap=market_cap)
        except ValueError:
            flash(f'* oof * No coin named “{coin}” here. Check spelling & API id and try again.', 'danger')
            return redirect(url_for('main.search'))
    
    return render_template('search.html')

@main.route('/profile')
@login_required
def profile():
    user = current_user
    return render_template('profile.html', user=user)
