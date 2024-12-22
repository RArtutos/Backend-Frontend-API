from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from ..services.accounts import AccountService
from ..forms.account import AccountForm
import json

bp = Blueprint('accounts', __name__)
account_service = AccountService()

@bp.route('/')
@login_required
def list():
    try:
        accounts = account_service.get_all()
        return render_template('accounts/list.html', accounts=accounts)
    except Exception as e:
        flash(f'Error loading accounts: {str(e)}', 'error')
        return render_template('accounts/list.html', accounts=[])

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = AccountForm()
    if form.validate_on_submit():
        try:
            account_data = form.get_data()
            result = account_service.create(account_data)
            if result:
                flash('Account created successfully', 'success')
                return redirect(url_for('accounts.list'))
            else:
                flash('Failed to create account', 'error')
        except Exception as e:
            flash(str(e), 'error')
    
    return render_template('accounts/form.html', form=form, is_edit=False)

@bp.route('/<int:account_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(account_id):
    account = account_service.get_by_id(account_id)
    if not account:
        flash('Account not found', 'error')
        return redirect(url_for('accounts.list'))
    
    form = AccountForm()
    if request.method == 'GET':
        form.name.data = account['name']
        form.group.data = account.get('group', '')
        form.max_concurrent_users.data = account.get('max_concurrent_users', 1)
        
        # Get domain from first cookie
        cookies = account.get('cookies', [])
        if cookies:
            form.domain.data = cookies[0].get('domain', '')
            if cookies[0].get('name') == 'header_cookies':
                form.cookies.data = cookies[0].get('value', '')
    
    if form.validate_on_submit():
        try:
            account_data = form.get_data()
            account_service.update(account_id, account_data)
            flash('Account updated successfully', 'success')
            return redirect(url_for('accounts.list'))
        except Exception as e:
            flash(str(e), 'error')
    
    return render_template('accounts/form.html', form=form, is_edit=True)

@bp.route('/<int:account_id>/delete', methods=['POST'])
@login_required
def delete(account_id):
    try:
        if account_service.delete(account_id):
            return jsonify({'success': True, 'message': 'Account deleted successfully'})
        return jsonify({'success': False, 'message': 'Failed to delete account'}), 400
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500