from __future__ import annotations

from pathlib import Path

from flask import (
    Flask,
    Response,
    current_app,
    g,
    jsonify,
    request,
    send_file,
    session,
)

from src.shared.time.timestamps import now_utc_iso

from ..features.user_sessions.models.user_session_event import (
    UserSessionEvent,
)
from .auth.request_identity import SESSION_IDENTITY_KEY
from .dependencies import (
    get_identity_sync_service,
    get_user_session_tracking_service,
)
from .env_configuration import EnvConfiguration

APPLE_TOUCH_ICON_FILES = {
    'apple-touch-icon.png': 'apple-touch-icon-180x180.png',
    'apple-touch-icon-precomposed.png': 'apple-touch-icon-180x180.png',
    'apple-touch-icon-120x120.png': 'apple-touch-icon-120x120.png',
    'apple-touch-icon-120x120-precomposed.png': 'apple-touch-icon-120x120.png',
    'apple-touch-icon-152x152.png': 'apple-touch-icon-152x152.png',
    'apple-touch-icon-152x152-precomposed.png': 'apple-touch-icon-152x152.png',
    'apple-touch-icon-167x167.png': 'apple-touch-icon-167x167.png',
    'apple-touch-icon-167x167-precomposed.png': 'apple-touch-icon-167x167.png',
    'apple-touch-icon-180x180.png': 'apple-touch-icon-180x180.png',
    'apple-touch-icon-180x180-precomposed.png': 'apple-touch-icon-180x180.png',
}


def register_routes(app: Flask, settings: EnvConfiguration) -> None:
    @app.route('/<path:path>', methods=['OPTIONS'])
    def handle_options(_: str):
        response = app.make_response('')
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type,Authorization',
        )
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET,PUT,POST,DELETE,OPTIONS',
        )
        return response

    @app.route('/health', methods=['GET'])
    def heartbeat():
        session.modified = True
        return jsonify({'status': 'UP'}), 200

    @app.post('/api/identity/register-current-user')
    def register_current_user():
        identity: dict | None = session.get(SESSION_IDENTITY_KEY)

        if not identity:
            return jsonify(
                {
                    'ok': False,
                    'registered': False,
                    'reason': 'unauthorized',
                }
            ), 401

        if not identity.get('needs_registration'):
            return jsonify(
                {
                    'ok': True,
                    'registered': False,
                    'reason': 'already_known',
                }
            ), 200

        registered = get_identity_sync_service().register_missing_identity(
            identity=identity,
        )

        if registered:
            identity['needs_registration'] = False
            session[SESSION_IDENTITY_KEY] = identity
            session.modified = True

            return jsonify(
                {
                    'ok': True,
                    'registered': True,
                    'reason': 'registered',
                }
            ), 200

        return jsonify(
            {
                'ok': True,
                'registered': False,
                'reason': 'not_registered',
            }
        ), 200

    @app.post('/api/user-session/touch')
    def touch_user_session():
        identity = getattr(g, 'identity', None)

        if identity is None:
            return jsonify(
                {
                    'status': 'unauthorized',
                    'tracked': False,
                }
            ), 401

        payload = request.get_json(silent=True) or {}

        event = UserSessionEvent.from_payload(
            payload=payload,
        )

        if event is None:
            return jsonify(
                {
                    'status': 'invalid_payload',
                    'tracked': False,
                }
            ), 400

        result = get_user_session_tracking_service().touch(
            identity=identity,
            event=event,
        )

        return jsonify(result), 200

    @app.route('/service-worker.js')
    def service_worker():
        assets_path = _get_assets_path()
        service_worker_path = assets_path / 'service-worker.js'

        app_version = _read_app_version(
            assets_path=assets_path,
        )

        content = service_worker_path.read_text(encoding='utf-8')
        content = content.replace('__APP_VERSION__', app_version)

        response = Response(
            response=content,
            status=200,
            mimetype='application/javascript',
        )

        response.headers['Service-Worker-Allowed'] = '/'
        _set_no_cache_headers(response=response)

        return response

    @app.route('/manifest.webmanifest')
    def web_manifest():
        manifest_path = _get_assets_path() / 'manifest.webmanifest'

        content = manifest_path.read_text(encoding='utf-8')

        response = Response(
            response=content,
            status=200,
            mimetype='application/manifest+json',
        )

        response.headers['Content-Type'] = 'application/manifest+json; charset=utf-8'
        _set_no_cache_headers(response=response)

        return response

    @app.route('/apple-touch-icon.png')
    @app.route('/apple-touch-icon-precomposed.png')
    @app.route('/apple-touch-icon-120x120.png')
    @app.route('/apple-touch-icon-120x120-precomposed.png')
    @app.route('/apple-touch-icon-152x152.png')
    @app.route('/apple-touch-icon-152x152-precomposed.png')
    @app.route('/apple-touch-icon-167x167.png')
    @app.route('/apple-touch-icon-167x167-precomposed.png')
    @app.route('/apple-touch-icon-180x180.png')
    @app.route('/apple-touch-icon-180x180-precomposed.png')
    def serve_apple_touch_icon():
        public_name = request.path.lstrip('/')

        filename = APPLE_TOUCH_ICON_FILES.get(public_name)

        if not filename:
            return 'Not found', 404

        icon_path = _get_assets_path() / 'img' / 'branding' / 'logos' / filename

        if not icon_path.exists():
            return 'Not found', 404

        response = send_file(
            icon_path,
            mimetype='image/png',
            max_age=0,
            conditional=False,
            as_attachment=False,
        )

        _set_no_cache_headers(response=response)

        return response

    @app.get('/health/live')
    def health_live():
        return jsonify({'status': 'ok', 'timestamp_utc': now_utc_iso()}), 200


def _get_assets_path() -> Path:
    return Path(current_app.root_path).parent / 'assets'


def _read_app_version(
    *,
    assets_path: Path,
) -> str:
    version_path = assets_path / 'version.txt'

    try:
        version = version_path.read_text(encoding='utf-8').strip()
    except Exception:
        return 'local'

    return version or 'local'


def _set_no_cache_headers(
    *,
    response,
) -> None:
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    response.headers['X-Content-Type-Options'] = 'nosniff'
