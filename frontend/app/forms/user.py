from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, IntegerField, SelectField
from wtforms.validators import DataRequired, Email, Length, Optional, NumberRange

class UserForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    is_admin = BooleanField('Is Admin')
    max_devices = IntegerField('Max Devices', 
                             validators=[DataRequired(), NumberRange(min=1)],
                             default=1)
    expires_in_days = IntegerField('Expires In (Days)', 
                                 validators=[Optional(), NumberRange(min=1)],
                                 default=30)
    preset_id = SelectField('Preset', 
                          validators=[Optional()],
                          coerce=int,
                          choices=[])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from ..services.admin import AdminService
        admin_service = AdminService()
        try:
            presets = admin_service.get_presets()
            self.preset_id.choices = [(0, 'None')] + [(p['id'], p['name']) for p in presets]
        except Exception:
            self.preset_id.choices = [(0, 'None')]
            
    def get_data(self):
        """Get form data in the format expected by the API"""
        data = {
            'email': self.email.data,
            'password': self.password.data,
            'is_admin': self.is_admin.data,
            'max_devices': self.max_devices.data,
            'expires_in_days': self.expires_in_days.data
        }
        
        if self.preset_id.data and self.preset_id.data != 0:
            data['preset_id'] = self.preset_id.data
            
        return data