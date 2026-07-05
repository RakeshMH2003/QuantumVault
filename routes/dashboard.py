from flask import Blueprint, render_template
from flask_login import login_required, current_user
from models.models import EncryptedData, ActivityLog
from sqlalchemy import func

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/dashboard')
@login_required
def index():
    uid = current_user.id

    total_encrypted = EncryptedData.query.filter_by(owner_id=uid).count()
    total_decrypted = ActivityLog.query.filter_by(user_id=uid, action='DECRYPT').count()
    total_downloads = ActivityLog.query.filter_by(user_id=uid, action='DOWNLOAD').count()

    recent_logs = (ActivityLog.query.filter_by(user_id=uid)
                              .order_by(ActivityLog.timestamp.desc())
                              .limit(10).all())

    recent_encrypted = (EncryptedData.query.filter_by(owner_id=uid)
                                     .order_by(EncryptedData.created_at.desc())
                                     .limit(5).all())

    return render_template('dashboard.html',
        total_encrypted=total_encrypted,
        total_decrypted=total_decrypted,
        total_downloads=total_downloads,
        recent_logs=recent_logs,
        recent_encrypted=recent_encrypted,
    )
