from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user
from ..services.auth import AuthService
from ..forms.auth import LoginForm

bp = Blueprint('auth', __name__)
auth_service = AuthService()

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('accounts.list'))
        
    form = LoginForm()
    if form.validate_on_submit():
        user, error = auth_service.login(form.email.data, form.password.data)
        
        if user:
            login_user(user)
            flash('Login successful', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('accounts.list'))
        else:
            flash(error or 'Login failed', 'error')
    
    return render_template('auth/login.html', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    flash('Logged out successfully', 'success')
    return redirect(url_for('auth.login'))