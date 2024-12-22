from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectMultipleField
from wtforms.validators import DataRequired

class PresetForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Description')
    account_ids = SelectMultipleField('Accounts', 
                                    validators=[DataRequired()],
                                    coerce=int)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from ..services.accounts import AccountService
        account_service = AccountService()
        accounts = account_service.get_all()
        self.account_ids.choices = [(a['id'], a['name']) for a in accounts]