from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required
from models.models import db, User, EncryptedData, ActivityLog
from utils.authentication import admin_required

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.route('/')
@login_required
@admin_required
def dashboard():
    total_users     = User.query.count()
    total_encrypted = EncryptedData.query.count()
    total_decrypts  = ActivityLog.query.filter_by(action='DECRYPT').count()
    total_downloads = ActivityLog.query.filter_by(action='DOWNLOAD').count()

    recent_logs = (ActivityLog.query
                   .order_by(ActivityLog.timestamp.desc())
                   .limit(30).all())

    # QRC-related activity only (ENCRYPT / DECRYPT / DOWNLOAD with a QRC code)
    qrc_logs = (ActivityLog.query
                .filter(ActivityLog.qrc_code.isnot(None))
                .order_by(ActivityLog.timestamp.desc())
                .limit(50).all())

    users = User.query.order_by(User.created_at.desc()).all()

    return render_template('admin.html',
        total_users=total_users,
        total_encrypted=total_encrypted,
        total_decrypts=total_decrypts,
        total_downloads=total_downloads,
        recent_logs=recent_logs,
        qrc_logs=qrc_logs,
        users=users,
    )


@admin_bp.route('/transactions')
@login_required
@admin_required
def transactions():
    page = request.args.get('page', 1, type=int)
    logs = (ActivityLog.query
            .order_by(ActivityLog.timestamp.desc())
            .paginate(page=page, per_page=25))
    return render_template('admin_transactions.html', logs=logs)


@admin_bp.route('/toggle-user/<int:uid>', methods=['POST'])
@login_required
@admin_required
def toggle_user(uid):
    user = User.query.get_or_404(uid)
    if user.role == 'admin':
        flash('Cannot disable admin accounts.', 'warning')
    else:
        user.is_active = not user.is_active
        db.session.commit()
        state = 'enabled' if user.is_active else 'disabled'
        flash(f'User "{user.username}" has been {state}.', 'info')
    return redirect(url_for('admin.dashboard'))
