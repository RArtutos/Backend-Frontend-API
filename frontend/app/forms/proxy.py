from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField
from wtforms.validators import DataRequired

class ProxyForm(FlaskForm):
    host = StringField('Host', validators=[DataRequired()])
    port = IntegerField('Port', validators=[DataRequired()])
    username = StringField('Username')
    password = StringField('Password')
    type = SelectField('Type', choices=[('https', 'HTTPS'), ('socks5', 'SOCKS5')])