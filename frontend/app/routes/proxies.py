from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required
from ..services.proxies import ProxyService
from ..forms.proxy import ProxyForm

bp = Blueprint('proxies', __name__)
proxy_service = ProxyService()

@bp.route('/proxies')
@login_required
def list():
    proxies = proxy_service.get_all()
    return render_template('proxies/list.html', proxies=proxies)

@bp.route('/proxies/create', methods=['GET', 'POST'])
@login_required
def create():
    form = ProxyForm()
    if form.validate_on_submit():
        try:
            proxy_service.create(form.data)
            flash('Proxy created successfully', 'success')
            return redirect(url_for('proxies.list'))
        except Exception as e:
            flash(str(e), 'error')
    
    return render_template('proxies/form.html', form=form)