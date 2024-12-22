from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, URLField
from wtforms.validators import DataRequired, NumberRange, ValidationError, Optional, URL
from datetime import datetime

class AccountForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    group = StringField('Group')
    domain = StringField('Domain', validators=[DataRequired()])
    cookies = TextAreaField('Cookies')
    max_concurrent_users = IntegerField('Maximum Concurrent Users', 
                                      validators=[DataRequired(), NumberRange(min=1)],
                                      default=1)
    image_url = URLField('Image URL', validators=[Optional(), URL()],
                        description="URL to an image representing this account (PNG format recommended)")

    def validate_domain(self, field):
        if not field.data:
            return
        
        domain = field.data.strip()
        if not domain.startswith('.') and not domain.startswith('http'):
            field.data = '.' + domain

        if domain.startswith('http'):
            from urllib.parse import urlparse
            domain = urlparse(domain).netloc
            field.data = '.' + domain if not domain.startswith('.') else domain

    def validate_cookies(self, field):
        if not field.data:
            return
            
        try:
            # Store cookies as a single header string
            field.processed_cookies = [{
                'domain': self.domain.data.strip(),
                'name': 'header_cookies',
                'value': field.data.strip(),
                'path': '/'
            }]
        except Exception as e:
            raise ValidationError(f'Error processing cookies: {str(e)}')

    def get_data(self):
        """Get form data in the format expected by the API"""
        cookies = getattr(self.cookies, 'processed_cookies', [])
        
        return {
            'name': self.name.data,
            'group': self.group.data or None,
            'cookies': cookies,
            'max_concurrent_users': self.max_concurrent_users.data,
            'image_url': self.image_url.data or None
        }