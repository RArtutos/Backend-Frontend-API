from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from ..services.admin import AdminService
from ..forms.user import UserForm
from ..core.auth import admin_required

bp = Blueprint('admin', __name__, url_prefix='/admin')
admin_service = AdminService()

@bp.route('/users')
@login_required
@admin_required
def list_users():
    users = admin_service.get_users()
    return render_template('admin/users/list.html', users=users)

@bp.route('/users/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_user():
    form = UserForm()
    if form.validate_on_submit():
        try:
            admin_service.create_user(form.data)
            flash('User created successfully', 'success')
            return redirect(url_for('admin.list_users'))
        except Exception as e:
            flash(str(e), 'error')
    return render_template('admin/users/form.html', form=form)

@bp.route('/users/<user_id>/accounts')
@login_required
@admin_required
def user_accounts(user_id):
    user = admin_service.get_user(user_id)
    accounts = admin_service.get_user_accounts(user_id)
    available_accounts = admin_service.get_available_accounts()
    return render_template('admin/users/accounts.html', 
                         user=user, 
                         accounts=accounts,
                         available_accounts=available_accounts)

@bp.route('/users/<user_id>/accounts/<int:account_id>', methods=['POST'])
@login_required
@admin_required
def assign_account(user_id, account_id):
    try:
        result = admin_service.assign_account_to_user(user_id, account_id)
        if result:
            return jsonify({'success': True, 'message': 'Account assigned successfully'})
        return jsonify({'success': False, 'message': 'Failed to assign account'}), 400
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@bp.route('/users/<user_id>/accounts/<int:account_id>', methods=['DELETE'])
@login_required
@admin_required
def remove_account(user_id, account_id):
    try:
        result = admin_service.remove_account_from_user(user_id, account_id)
        if result:
            return jsonify({'success': True, 'message': 'Account removed successfully'})
        return jsonify({'success': False, 'message': 'Failed to remove account'}), 400
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500