from flask import Blueprint, render_template, abort
from flask_login import login_required, current_user
from ..services.analytics import AnalyticsService
from ..core.auth import admin_required

bp = Blueprint('analytics', __name__, url_prefix='/analytics')
analytics_service = AnalyticsService()

@bp.route('/user/<user_id>')
@login_required
def user_analytics(user_id):
    if not current_user.is_admin and current_user.email != user_id:
        abort(403)
    analytics_data = analytics_service.get_user_analytics(user_id)
    return render_template('analytics/user_dashboard.html', analytics=analytics_data)

@bp.route('/account/<int:account_id>')
@login_required
def account_analytics(account_id):
    analytics_data = analytics_service.get_account_analytics(account_id)
    return render_template('analytics/account_dashboard.html', analytics=analytics_data)

@bp.route('/dashboard')
@login_required
@admin_required
def analytics_dashboard():
    analytics_data = analytics_service.get_dashboard_analytics()
    return render_template('analytics/dashboard.html', analytics=analytics_data)
