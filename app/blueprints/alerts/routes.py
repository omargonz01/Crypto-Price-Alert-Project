from . import alerts
from .forms import AlertForm
from flask import request, redirect, url_for, render_template, flash, Flask, jsonify
from flask_login import current_user, login_required
from dotenv import load_dotenv
from mailjet_rest import Client
from pytz import timezone
from datetime import datetime
from app.models import db, Alert, User
import requests, os



load_dotenv()

@alerts.route('/set_alert',  methods=['GET', 'POST'])
@login_required
def set_alert():
    form = AlertForm()
    if request.method == 'POST' and form.validate_on_submit():
        coin_name = form.coin_name.data
        currency = form.currency.data
        price = form.price.data
        direction = form.direction.data
        channel = form.channel.data
        exchange = form.exchange.data

        url = "https://cryptocurrencyalerting.com/api/v1/alerts"

        # Define the headers for the API request
        headers = {
            "Content-Type": "application/json",
            "X-Api-Key": os.getenv("API_KEY")
        }
        
        data = {
        "type": "price",
        "currency": coin_name,
        "target_currency": currency,
        "price": price,
        "direction": direction,
        "channel": {"name": channel},
        "exchange": exchange
        }

         # Send the API request
        response = requests.post(url, headers=headers, json=data)

        
        new_alert = Alert(crypto_name=coin_name, price=price, direction=direction, channel=channel, user_id=current_user.id)

        db.session.add(new_alert)
        db.session.commit()

        flash(f"Nice, {current_user.first_name}! New alert for { coin_name.title() } has been set 🎊", 'success')
        return redirect(url_for('alerts.my_alerts'))

    else:
        return render_template('set_alert.html', form=form)
    
@alerts.route('/all_alerts')
def all_alerts():
    alerts = Alert.query.all()

    # Convert the UTC timestamps to Pacific Time (PT) and format date and time
    pacific = timezone('US/Pacific')
    for alert in alerts:
        alert.date_created = alert.date_created.astimezone(pacific)
        alert.date_created_str = alert.date_created.strftime('%Y-%m-%d')
        alert.time_created_str = alert.date_created.strftime('%H:%M:%S')

    return render_template('all_alerts.html', alerts=alerts)

@alerts.route('/my_alerts')
@login_required
def my_alerts():
   
    alerts = Alert.query.filter_by(user_id=current_user.id).all()
    alerts = Alert.query.filter_by(user_id=current_user.id).all()
    pacific = timezone('US/Pacific')
    for alert in alerts:
        
        alert.date_created = alert.date_created.astimezone(pacific)
        alert.date_created_str = alert.date_created.strftime('%Y-%m-%d')
        alert.time_created_str = alert.date_created.strftime('%H:%M:%S')

    return render_template('my_alerts.html', alerts=alerts)

@alerts.route('/update/<int:alert_id>', methods=['GET','POST'])
@login_required
def update_alert(alert_id):
    alert = Alert.query.get(alert_id)
    form = AlertForm()

    if request.method == 'POST':

        coin_name = form.coin_name.data
        price = form.price.data
        direction = form.direction.data
        channel = form.channel.data

        alert.coin_name = coin_name
        alert.price = price
        alert.direction = direction
        alert.channel = channel

        db.session.commit()

        return redirect(url_for('alerts.my_alerts'))
    
    else:
        return render_template('update_alert.html', alert=alert, form=form)

@alerts.route('/delete/<int:alert_id>', methods=['GET', 'POST'])
@login_required
def delete_alert(alert_id):
    alert = Alert.query.get(alert_id)

    db.session.delete(alert)
    db.session.commit()

    flash(f'Successfully deleted your {alert.crypto_name.title()} alert!', 'success')
    return redirect(url_for('alerts.all_alerts'))


@alerts.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    alert_id = data['alert_id']
    alert = Alert.query.get(alert_id)
    user = User.query.get(alert.user_id)

    # Set up Mailjet
    mailjet_api_key = os.getenv("MAILJET_API_KEY")
    api_secret = os.getenv("MAILJET_API_SECRET")
    mailjet = Client(auth=(mailjet_api_key, api_secret), version='v3.1')

    # Format a message
    message = {
        'Messages': [
            {
                "From": {
                    "Email": "help@ogwholesaling.com",
                    "Name": "Degen Zone"
                },
                "To": [
                    {
                        "Email": user.email,
                        "Name": f"{user.first_name} {user.last_name}"
                    }
                ],
                "Subject": f"{alert.crypto_name.title()} Price Alert",
                "TextPart": f"Your alert for {alert.crypto_name} has been triggered.",
                "HTMLPart": f"<h3>Your alert for {alert.crypto_name.title()} has been triggered.</h3><br />The current price is ${data['current_price']}. Do with this information what you will.",
                "CustomID": "AlertTriggered"
            }
        ]
    }

    # Send the email
    result = mailjet.send.create(data=message)
    print(result.status_code)
    print(result.json())

    return jsonify({
        'status': 'success',
        'message': f"Alert Triggered: {alert.crypto_name}"
    })



# @alerts.route('/alerts', methods=['GET'])
# def get_all_alerts():
#     headers = {"X-Api-Key": API_KEY}
#     response = requests.get(API_URL, headers=headers)
#     return jsonify(response.json()), 200

# @alerts.route('/alerts/<int:alert_id>', methods=['GET'])
# def get_alert(alert_id):
#     headers = {"X-Api-Key": API_KEY}
#     response = requests.get(f"{API_URL}/{alert_id}", headers=headers)
#     return jsonify(response.json()), 200

# @alerts.route('/alerts/<int:alert_id>/enable', methods=['POST'])
# def enable_alert(alert_id):
#     headers = {"X-Api-Key": API_KEY}
#     response = requests.post(f"{API_URL}/{alert_id}/enable", headers=headers)
#     return jsonify(response.json()), 200

# @alerts.route('/alerts/<int:alert_id>/disable', methods=['POST'])
# def disable_alert(alert_id):
#     headers = {"X-Api-Key": API_KEY}
#     response = requests.post(f"{API_URL}/{alert_id}/disable", headers=headers)
#     return jsonify(response.json()), 200

# @alerts.route('/alerts/<int:alert_id>', methods=['DELETE'])
# def delete_alerts(alert_id):
#     headers = {"X-Api-Key": API_KEY}
#     response = requests.delete(f"{API_URL}/{alert_id}", headers=headers)
#     return jsonify(response.json()), 200