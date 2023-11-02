from . import auth
from .forms import LoginForm, SignupForm, ResetPasswordForm, ResetPasswordConfirmForm
from flask import request, flash, redirect, url_for, render_template
from app.models import User, db, ResetRequest
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, logout_user, current_user
import secrets 
from datetime import datetime
from mailjet_rest import Client
import os

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if request.method == 'POST' and form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data.lower()
        password = form.password.data
        
        new_user = User(first_name, last_name, email, password)

        db.session.add(new_user)
        db.session.commit()
        flash(f"Congratulations {new_user.first_name}! You’re now a certified Degen 🎊 Login to enter The Degen Zone", 'success')
        return redirect(url_for('auth.login'))

    else:
        return render_template('signup.html', form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data.lower()
        password = form.password.data
        queried_user = User.query.filter(User.email == email).first()
        if queried_user and check_password_hash(queried_user.password, password):
            login_user(queried_user)
            flash(f"You've successfully entered the Degen Zone, {queried_user.first_name}. Remember, what happens in the Degen Zone, stays in the Degen Zone! 🤫",'success')
            return redirect(url_for('main.search'))
        else:
            flash(f'Invalid email or password combination', 'danger')
            return redirect(url_for('login'))
    else:
        return render_template('login.html', form=form)  

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@auth.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    form = ResetPasswordForm()
    if form.validate_on_submit():
        email = form.email.data 
        user = User.query.filter_by(email=email).first()
        if user:
            secret_key = secrets.token_urlsafe(16)
            reset_request = ResetRequest(secret_key=secret_key,  user_id=user.id) 
            db.session.add(reset_request) 
            db.session.commit()
            reset_url = url_for('auth.reset_password_confirm', secret_key=secret_key, _external=True)
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
                        "Subject": "Password Reset",
                        "TextPart": f"Hello there,\n\nWe've received your request to reset your password for Degen Zone. To get back on track, simply click on the link below:\n\n{reset_url}\n\n If you didn't request this, no worries - just disregard this message.\n\nBest regards,\nYour friends at Degen Zone",
                        "HTMLPart": f"<h3>Hello there!</h3><br /><p>We noticed that you've requested to reset your password for Degen Zone. Don't worry; we've got you covered. Just click the button below to reset your password:</p><br /><a href='{reset_url}'><button style='background-color: #4CAF50; color: white; border: none; padding: 10px 20px; text-align: center; text-decoration: none; display: inline-block; font-size: 16px; margin: 4px 2px; cursor: pointer; border-radius: 5px;'>Reset Password</button></a><br /><p>If you didn't initiate this request, please ignore this message, and your account will remain secure.</p><br /><p>Warm regards,<br />Your friends at Degen Zone</p>",
                        "CustomID": "PasswordReset"
                    }
                ]
            }
            # Send the email
            result = mailjet.send.create(data=message)
            print(result.status_code)
            print(result.json())
            flash('An email has been sent to you with instructions to reset your password.', 'success')
            logout_user()
        else:
            flash('This email is not registered.', 'danger')
        return redirect(url_for('auth.login'))
    return render_template('/reset_password.html', form=form)

@auth.route('/reset_password_confirm/<secret_key>', methods=['GET', 'POST'])
def reset_password_confirm(secret_key):
    form = ResetPasswordConfirmForm()
    reset_request = ResetRequest.query.filter_by(secret_key=secret_key).first()
    if reset_request:
        user = reset_request.user
        if form.validate_on_submit():
            new_password = form.new_password.data
            user.password = generate_password_hash(new_password)
            db.session.delete(reset_request)
            db.session.commit()
            flash('Your password has been updated.')
            return redirect(url_for('auth.login'))
        return render_template('reset_password_confirm.html', form=form, secret_key=secret_key)
    else:
        flash('Invalid or expired token.')
        return redirect(url_for('auth.reset_password'))

