from . import auth
from .forms import LoginForm, SignupForm
from flask import request, flash, redirect, url_for, render_template
from app.models import User, db
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, current_user

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