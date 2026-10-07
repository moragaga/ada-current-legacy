from __future__ import annotations

from flask import Blueprint, jsonify

from ..auth.identity_context import get_current_identity, get_current_profile

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/me', methods=['GET'])
def me():
    return jsonify(
        {
            'identity': get_current_identity(),
            'profile': get_current_profile(),
        }
    ), 200
