from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, SubmitField, StringField 
from wtforms.validators import DataRequired, EqualTo, Email
from flask import Flask, render_template, redirect, url_for, flash 
from wtforms import StringField, SubmitField

class LoginForm(FlaskForm):
    email = EmailField('Email Address: ', validators=[DataRequired()], render_kw={"required": True})
    password = PasswordField('Password: ', validators=[DataRequired()], render_kw={"required": True})
    submit_btn = SubmitField('Sign In')

class SignupForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()], render_kw={"required": True})
    last_name = StringField('Last Name', validators=[DataRequired()], render_kw={"required": True})
    email = EmailField('Email Address: ', validators=[DataRequired()], render_kw={"required": True})
    password = PasswordField('Password: ', validators=[DataRequired()], render_kw={"required": True})
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')], render_kw={"required": True})
    submit_btn = SubmitField('Register')

class CryptoForm(FlaskForm):
    cryptoCoinName = StringField('Enter a Cryptocurrency: ', validators=[DataRequired()])

class ResetPasswordForm(FlaskForm):
    email = EmailField('Email:', validators=[DataRequired()])
    submit = SubmitField('Request Password Reset') 

class ResetPasswordConfirmForm(FlaskForm):
    new_password = PasswordField('New Password', validators=[DataRequired()])
    new_password_confirm = PasswordField('Confirm New Password', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Reset Password')