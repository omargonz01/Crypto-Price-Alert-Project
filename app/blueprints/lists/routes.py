from . import lists
from .forms import AddCryptoForm
from flask import request, redirect, url_for, render_template, flash, jsonify
from flask_login import current_user, login_required
from app.models import db, CryptoList, Crypto, UserCrypto
import requests

@lists.route('/add_to_list/<crypto_name>', methods=['POST'])
@login_required
def add_to_list(crypto_name):
    # Extract cryptocurrency information from POST data
    coin_name = request.form.get('coin_name')
    coin_symbol = request.form.get('coin_symbol')
    all_time_high = float(request.form.get('all_time_high'))
    current_price = float(request.form.get('current_price'))
    market_cap = float(request.form.get('market_cap'))

    # Get or create the user's list
    crypto_list = CryptoList.query.filter_by(user_id=current_user.id).first()
    if not crypto_list:
        crypto_list = CryptoList(name="My List", user_id=current_user.id)
        db.session.add(crypto_list)
        db.session.commit()

    # Add the cryptocurrency to the list
    crypto = Crypto(
        name=coin_name,
        symbol=coin_symbol,
        all_time_high_price=all_time_high,
        current_price=current_price,
        market_cap=market_cap,
        list_id=crypto_list.id
    )
    db.session.add(crypto)
    db.session.commit()

    return jsonify({'success': True, 'crypto_name': coin_name})

@lists.route('/added_to_list/<crypto_name>', methods=['POST'])
@login_required
def added_to_list(crypto_name):
    
    coin_name = request.form.get('coin_name')
    coin_symbol = request.form.get('coin_symbol')
    all_time_high = float(request.form.get('all_time_high'))
    current_price = float(request.form.get('current_price'))
    market_cap = float(request.form.get('market_cap'))

    
    crypto_list = CryptoList.query.filter_by(user_id=current_user.id).first()
    if not crypto_list:
        crypto_list = CryptoList(name="My List", user_id=current_user.id)
        db.session.add(crypto_list)
        db.session.commit()

    # Add the cryptocurrency to the list
    crypto = Crypto(
        name=coin_name,
        symbol=coin_symbol,
        all_time_high_price=all_time_high,
        current_price=current_price,
        market_cap=market_cap,
        list_id=crypto_list.id
    )
    db.session.add(crypto)
    db.session.commit()
    flash(f"It's lit 🔥! {coin_name.title()} has been added to your list. 😎", 'success')

    return redirect(url_for('lists.my_list'))
    

@lists.route('/my_list', methods=['GET'])
@login_required
def my_list():
    # Get the user's list of cryptocurrencies
    user = current_user  # Get the current user
    crypto_list = CryptoList.query.filter_by(user_id=user.id).first()

    if crypto_list:
        cryptos = Crypto.query.filter_by(list_id=crypto_list.id).all()
    else:
        cryptos = []

    def get_crypto_notes(crypto_id):
        user_crypto = UserCrypto.query.filter_by(user_id=user.id, crypto_id=crypto_id).first()
        if user_crypto:
            return user_crypto.notes
        return ""

    return render_template('my_list.html', cryptos=cryptos, get_crypto_notes=get_crypto_notes)

@lists.route('/remove_from_list/<int:crypto_id>', methods=['POST'])
@login_required
def remove_from_list(crypto_id):
    # Get the crypto
    crypto = Crypto.query.get(crypto_id)

    # Check if the crypto exists and belongs to the current user
    if crypto and crypto.list.user_id == current_user.id:
        db.session.delete(crypto)
        db.session.commit()
        flash(f"{crypto.name.title()} has been removed from your list! 😮", 'success')
    else:
        flash("Failed to remove cryptocurrency from list.", 'danger')

    return redirect(url_for('lists.my_list'))

@lists.route('/view_notes')
@login_required
def view_notes():
    user = current_user  
    user_cryptos = UserCrypto.query.filter_by(user_id=user.id).all()


    return render_template('view_notes.html', user_cryptos=user_cryptos)

@lists.route('/view_my_notes', methods=['GET', 'POST'])
@login_required
def view_my_notes():
    if request.method == 'POST':
        try:
            data = request.get_json()
            crypto_id = data['crypto_id']
            new_notes = data['notes']

            user = current_user

            user_crypto = UserCrypto.query.filter_by(user_id=user.id, crypto_id=crypto_id).first()

            if user_crypto:
                user_crypto.notes = new_notes
                db.session.commit()
                return jsonify({'message': 'Notes updated successfully'})
            else:
                user_crypto = UserCrypto(user_id=user.id, crypto_id=crypto_id, notes=new_notes)
                db.session.add(user_crypto)
                db.session.commit()
                return jsonify({'message': 'Notes created successfully'})
        except Exception as e:
            return jsonify({'error': str(e)})

    user = current_user
    user_cryptos = UserCrypto.query.filter_by(user_id=user.id).all()
    return render_template('view_my_notes.html', user_cryptos=user_cryptos)

@lists.route('/update_crypto_notes/<int:crypto_id>', methods=['POST'])
@login_required
def update_crypto_notes(crypto_id):
    data = request.get_json()
    new_notes = data['notes']

    user = current_user

    user_crypto = UserCrypto.query.filter_by(user_id=user.id, crypto_id=crypto_id).first()

    if user_crypto:

        user_crypto.notes = new_notes
        db.session.commit()
        
        return jsonify({'message': 'Notes updated successfully'})
    else:
        # Create a new user-crypto relationship if it doesn't exist
        user_crypto = UserCrypto(user_id=user.id, crypto_id=crypto_id, notes=new_notes)
        db.session.add(user_crypto)
        db.session.commit()
        
        return jsonify({'message': 'Notes created successfully'})
    
@lists.route('/updated_crypto_notes/<int:crypto_id>', methods=['POST'])
@login_required
def updated_crypto_notes(crypto_id):
    try:
        data = request.get_json()
        new_notes = data['notes']

        user = current_user

        user_crypto = UserCrypto.query.filter_by(user_id=user.id, crypto_id=crypto_id).first()

        if user_crypto:
            user_crypto.notes = new_notes
            db.session.commit()
            return jsonify({'message': 'Notes updated successfully'})
        else:
            user_crypto = UserCrypto(user_id=user.id, crypto_id=crypto_id, notes=new_notes)
            db.session.add(user_crypto)
            db.session.commit()
            return jsonify({'message': 'Notes created successfully'})
    except Exception as e:
        return jsonify({'error': str(e)})
        


def get_coins_by_category(category):
    url = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&category={category}&order=market_cap_desc"
    response = requests.get(url)
    data = response.json()
    coins = []
    for coin in data:
        coins.append({
            'name': coin['name'],
            'symbol': coin['symbol'],
            'current_price': coin['current_price'],
            'all_time_high': coin['ath'],
            'market_cap': coin['market_cap']
        })
    return coins

@lists.route('/gaming')
def gaming():
    coins = get_coins_by_category('gaming')
    return render_template('gaming.html', coins=coins)

@lists.route('/meme')
def meme():
    coins = get_coins_by_category('meme-token')
    return render_template('meme.html', coins=coins)

@lists.route('/layer2')
def layer2():
    coins = get_coins_by_category('layer-2')
    return render_template('layer2.html', coins=coins)