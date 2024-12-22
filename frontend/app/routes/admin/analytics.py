"""Admin analytics routes"""
from flask import render_template
from flask_login import current_user
from ...services.admin import AdminService

admin_service = AdminService()

class AnalyticsViews:
    def analytics_dashboard(self):
        """Get general analytics dashboard"""
        analytics_data = admin_service.get_analytics()
        return render_template('admin/analytics.html', analytics=analytics_data)

    def user_analytics(self, user_id):
        """Get analytics for a specific user"""
        analytics_data = admin_service.get_user_analytics(user_id)
        user_data = admin_service.get_user(user_id)
        return render_template('analytics/user_dashboard.html', 
                             analytics=analytics_data,
                             user=user_data)

    def account_analytics(self, account_id):
        """Get analytics for a specific account"""
        analytics_data = admin_service.get_account_analytics(account_id)
        account = admin_service.get_account(account_id)
        return render_template('analytics/account_dashboard.html', 
                             analytics=analytics_data,
                             account=account)

analytics_views = AnalyticsViews()
