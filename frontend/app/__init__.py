from flask import Flask
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_session import Session
from datetime import timedelta
from .models.user import User

login_manager = LoginManager()
csrf = CSRFProtect()
flask_session = Session()

@login_manager.user_loader
def load_user(user_id):
    from .services.auth import AuthService
    auth_service = AuthService()
    return auth_service.get_user(user_id)

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')
    
    # Session configuration
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=24)
    app.config['SESSION_REFRESH_EACH_REQUEST'] = True
    
    with app.app_context():
        login_manager.init_app(app)
        csrf.init_app(app)
        flask_session.init_app(app)
        
        login_manager.login_view = 'auth.login'
        login_manager.login_message_category = 'info'
        
        # Import and register blueprints
        from .routes.auth import bp as auth_bp
        from .routes.accounts import bp as accounts_bp
        from .routes.proxies import bp as proxies_bp
        from .routes.admin import bp as admin_bp
        
        app.register_blueprint(auth_bp)
        app.register_blueprint(accounts_bp)
        app.register_blueprint(proxies_bp)
        app.register_blueprint(admin_bp)
    
    return app