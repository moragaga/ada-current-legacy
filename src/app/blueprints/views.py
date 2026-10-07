from __future__ import annotations

from flask import Blueprint, current_app, redirect, request, session

views_bp = Blueprint('views_bp', __name__)


@views_bp.route('/logout')
def logout():
    session.clear()
    if current_app.config.get('FLASK_ENV') == 'LOCAL':
        return redirect('/')

    return redirect('https://{0}/.auth/logout'.format(request.host))
