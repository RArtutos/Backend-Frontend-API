from flask import render_template, redirect, url_for, flash, request, jsonify
from ...services.admin import AdminService
from ...forms.user import UserForm

admin_service = AdminService()

class UserViews:
    def list_users(self):
        """List all users"""
        users = admin_service.get_users()
        return render_template('admin/users/list.html', users=users)

    def create_user(self):
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

    def edit_user(self, user_id):
        """Edit existing user"""
        user = admin_service.get_user(user_id)
        if not user:
            flash('User not found', 'error')
            return redirect(url_for('admin.admin_list_users'))

        form = UserForm()
        if request.method == 'GET':
            form.email.data = user['email']
            form.is_admin.data = user.get('is_admin', False)
            form.max_devices.data = user.get('max_devices', 1)
            form.preset_id.data = user.get('preset_id', 0)

        if form.validate_on_submit():
            try:
                if admin_service.update_user(user_id, form.get_data()):
                    flash('User updated successfully', 'success')
                    return redirect(url_for('admin.admin_list_users'))
                flash('Failed to update user', 'error')
            except Exception as e:
                flash(str(e), 'error')
        return render_template('admin/users/form.html', form=form, is_edit=True)

    def user_accounts(self, user_id):
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

    def assign_account(self, user_id, account_id):
        """Assign account to user"""
        try:
            if admin_service.assign_account_to_user(user_id, account_id):
                return jsonify({'success': True, 'message': 'Account assigned successfully'})
            return jsonify({'success': False, 'message': 'Failed to assign account'}), 400
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)}), 500

    def remove_account(self, user_id, account_id):
        """Remove account from user"""
        try:
            if admin_service.remove_account_from_user(user_id, account_id):
                return jsonify({'success': True, 'message': 'Account removed successfully'})
            return jsonify({'success': False, 'message': 'Failed to remove account'}), 400
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)}), 500

    def delete_user(self, user_id):
        """Delete user"""
        try:
            if admin_service.delete_user(user_id):
                return jsonify({'success': True, 'message': 'User deleted successfully'})
            return jsonify({'success': False, 'message': 'Failed to delete user'}), 400
        except Exception as e:
            return jsonify({'success': False, 'message': str(e)}), 500

user_views = UserViews()