from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SelectField, SubmitField
from wtforms.validators import DataRequired

class AlertForm(FlaskForm):
    coin_name = StringField('Coin Name', validators=[DataRequired()])
    currency = StringField('Currency', validators=[DataRequired()])
    price = FloatField('Price', validators=[DataRequired()])
    direction = SelectField('Direction', choices=[('', 'Price Direction'), ('above', 'Above'), ('below', 'Below')], validators=[DataRequired()])
    channel = SelectField('Channel', choices=[('', 'Alert Type'), ('sms', 'SMS'), ('email', 'Email')], validators=[DataRequired()])    
    exchange = SelectField('Exchange', choices=[('coinbase_pro', 'Coinbase Pro'), ('binance', 'Binance'), ('uniswap', 'UniSwap'), ('pancakeswap', 'PancakeSwap'), ('gate_io', 'Gate.io')], validators=[DataRequired()])
    submit = SubmitField('Set Alert')

