from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from functools import wraps
from flask import abort
from flask_login import current_user
from models.models import db, ActivityLog
from datetime import datetime

login_manager = LoginManager()
bcrypt        = Bcrypt()


@login_manager.user_loader
def load_user(user_id):
    from models.models import User
    return User.query.get(int(user_id))


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            abort(403)
        return f(*args, **kwargs)
    return decorated


def get_real_ip():
    """Extract real IP even if behind a proxy like Nginx or Cloudflare"""
    from flask import request
    if request.headers.getlist("X-Forwarded-For"):
        return request.headers.getlist("X-Forwarded-For")[0].split(',')[0].strip()
    return request.remote_addr

def log_activity(user_id: int, action: str, detail: str = None,
                 qrc_code: str = None, ip: str = None, status: str = 'SUCCESS'):
    """Write one row to ActivityLog."""
    try:
        if not ip:
            try:
                ip = get_real_ip()
            except RuntimeError: # If not in request context
                ip = 'System'

        entry = ActivityLog(
            user_id    = user_id,
            action     = action,
            detail     = detail,
            qrc_code   = qrc_code,
            ip_address = ip,
            status     = status,
            timestamp  = datetime.utcnow(),
        )
        db.session.add(entry)
        db.session.commit()
    except Exception:
        db.session.rollback()
