"""Admin views module containing all admin route handlers"""
from flask import render_template, redirect, url_for, flash, jsonify
from flask_login import login_required
from ...core.auth import admin_required
from ...services.admin import AdminService
from ...forms.user import UserForm
from ...forms.preset import PresetForm  # Add this import

admin_service = AdminService()

# Analytics views
def analytics_dashboard():
    """Get general analytics dashboard"""
    analytics_data = admin_service.get_analytics()
    return render_template('admin/analytics.html', analytics=analytics_data)

def user_analytics(user_id):
    """Get analytics for a specific user"""
    analytics_data = admin_service.get_user_analytics(user_id)
    return render_template('analytics/user_dashboard.html', analytics=analytics_data)

def account_analytics(account_id):
    """Get analytics for a specific account"""
    analytics_data = admin_service.get_account_analytics(account_id)
    return render_template('analytics/account_dashboard.html', analytics=analytics_data)

# User management views
def list_users():
    """List all users"""
    users = admin_service.get_users()
    return render_template('admin/users/list.html', users=users)

def create_user():
    """Create new user"""
    form = UserForm()
    if form.validate_on_submit():
        try:
            admin_service.create_user(form.data)
            flash('User created successfully', 'success')
            return redirect(url_for('admin.admin_list_users'))
        except Exception as e:
            flash(str(e), 'error')
    return render_template('admin/users/form.html', form=form)

def user_accounts(user_id):
    """Manage user accounts"""
    user = admin_service.get_user(user_id)
    if not user:
        flash('User not found', 'error')
        return redirect(url_for('admin.admin_list_users'))
        
    accounts = admin_service.get_user_accounts(user_id)
    available_accounts = admin_service.get_available_accounts()
    return render_template('admin/users/accounts.html', 
                         user=user, 
                         accounts=accounts,
                         available_accounts=available_accounts)

# Preset management views
def list_presets():
    """List all presets"""
    try:
        presets = admin_service.get_presets()
        return render_template('admin/presets/list.html', presets=presets)
    except Exception as e:
        flash(f'Error loading presets: {str(e)}', 'error')
        return render_template('admin/presets/list.html', presets=[])