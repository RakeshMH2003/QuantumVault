import secrets, string, io, mimetypes, base64
from datetime import datetime
from flask import Blueprint, render_template, request, flash, redirect, url_for, send_file
from flask_login import login_required, current_user
from models.models import db, EncryptedData
from utils.authentication import log_activity, get_real_ip
from utils.encryption import encrypt_data, decrypt_data

crypto_bp = Blueprint('crypto', __name__)


# ── Helpers ───────────────────────────────────────────────────────────────────

def _gen_qrc() -> str:
    chars = string.ascii_uppercase + string.digits
    while True:
        code = 'QRC-' + '-'.join(
            ''.join(secrets.choice(chars) for _ in range(4)) for _ in range(3)
        )
        if not EncryptedData.query.filter_by(qrc_code=code).first():
            return code


def _human_size(n: int) -> str:
    for u in ('B', 'KB', 'MB', 'GB'):
        if n < 1024: return f'{n:.1f} {u}'
        n /= 1024
    return f'{n:.1f} TB'


def _icon(mime: str) -> str:
    if 'pdf'   in mime: return '📄'
    if 'image' in mime: return '🖼️'
    if 'text'  in mime: return '📝'
    if 'word'  in mime or 'document'    in mime: return '📃'
    if 'sheet' in mime or 'spreadsheet' in mime: return '📊'
    if 'zip'   in mime or 'compressed'  in mime: return '🗜️'
    return '📁'


# ── ENCRYPT ───────────────────────────────────────────────────────────────────

@crypto_bp.route('/encrypt', methods=['GET', 'POST'])
@login_required
def encrypt_page():
    if request.method == 'POST':
        file        = request.files.get('file')
        plaintext   = request.form.get('plaintext', '').strip()
        description = request.form.get('description', '').strip()

        raw, fname, mime = None, None, 'application/octet-stream'

        if file and file.filename:
            raw   = file.read()
            fname = file.filename
            mime  = file.mimetype or mimetypes.guess_type(fname)[0] or mime
        elif plaintext:
            raw   = plaintext.encode('utf-8')
            fname = 'secure_message.txt'
            mime  = 'text/plain'
        else:
            flash('Please upload a file or enter a message to encrypt.', 'warning')
            return render_template('encrypt.html')

        try:
            enc   = encrypt_data(raw)
            code  = _gen_qrc()
            rec   = EncryptedData(
                owner_id=current_user.id,
                qrc_code=code,
                original_filename=fname,
                mime_type=mime,
                file_size=len(raw),
                encrypted_blob=enc,
                description=description or None,
            )
            db.session.add(rec)
            db.session.commit()
            log_activity(current_user.id, 'ENCRYPT',
                         f'Encrypted "{fname}" ({_human_size(len(raw))})',
                         qrc_code=code, ip=get_real_ip())
            return render_template('encrypt_success.html',
                code=code,
                fname=fname,
                size=_human_size(len(raw)),
                mime=mime,
                icon=_icon(mime),
                description=description,
                created=rec.created_at.strftime('%d %B %Y · %H:%M UTC'),
            )
        except Exception as e:
            db.session.rollback()
            flash(f'Encryption error: {e}', 'danger')

    return render_template('encrypt.html')


# ── DECRYPT ───────────────────────────────────────────────────────────────────

@crypto_bp.route('/decrypt', methods=['GET', 'POST'])
@login_required
def decrypt_page():
    result = None
    if request.method == 'POST':
        code = request.form.get('qrc_code', '').strip().upper()
        if not code:
            flash('Please enter a QRC code.', 'warning')
            return render_template('decrypt.html', result=None)

        rec = EncryptedData.query.filter_by(qrc_code=code).first()
        if not rec:
            log_activity(current_user.id, 'DECRYPT',
                         f'Invalid QRC code attempted: {code}',
                         qrc_code=code, ip=get_real_ip(), status='FAILED')
            flash('Invalid QRC code. Please check and try again.', 'danger')
        elif not rec.is_active:
            flash('This QRC code has been revoked by the sender.', 'warning')
        else:
            try:
                dec_bytes = decrypt_data(rec.encrypted_blob)

                rec.decrypt_count     += 1
                rec.last_decrypted_at  = datetime.utcnow()
                rec.last_decrypted_by  = current_user.id
                db.session.commit()

                log_activity(current_user.id, 'DECRYPT',
                             f'Decrypted "{rec.original_filename}" (QRC: {code})',
                             qrc_code=code, ip=get_real_ip())

                # Build preview
                mime = rec.mime_type
                preview_type = 'download'
                preview_data = None

                if mime.startswith('text/'):
                    preview_type = 'text'
                    preview_data = dec_bytes.decode('utf-8', errors='replace')
                elif mime.startswith('image/'):
                    preview_type = 'image'
                    preview_data = f'data:{mime};base64,' + base64.b64encode(dec_bytes).decode()
                elif 'pdf' in mime:
                    preview_type = 'pdf'
                    preview_data = 'data:application/pdf;base64,' + base64.b64encode(dec_bytes).decode()

                result = dict(
                    rec=rec,
                    preview_type=preview_type,
                    preview_data=preview_data,
                    icon=_icon(mime),
                    size=_human_size(rec.file_size),
                    sender=rec.owner,
                )
            except Exception as e:
                db.session.rollback()
                log_activity(current_user.id, 'DECRYPT',
                             f'Decryption failed for {code}: {e}',
                             qrc_code=code, ip=get_real_ip(), status='FAILED')
                flash(f'Decryption failed: {e}', 'danger')

    return render_template('decrypt.html', result=result)


# ── DOWNLOAD ──────────────────────────────────────────────────────────────────

@crypto_bp.route('/download/<code>')
@login_required
def download_file(code):
    rec = EncryptedData.query.filter_by(qrc_code=code.upper()).first_or_404()
    dec_bytes = decrypt_data(rec.encrypted_blob)
    log_activity(current_user.id, 'DOWNLOAD',
                 f'Downloaded "{rec.original_filename}" (QRC: {code})',
                 qrc_code=code, ip=get_real_ip())
    return send_file(
        io.BytesIO(dec_bytes),
        as_attachment=True,
        download_name=rec.original_filename,
        mimetype=rec.mime_type,
    )


# ── HISTORY ───────────────────────────────────────────────────────────────────

@crypto_bp.route('/history')
@login_required
def history():
    from models.models import ActivityLog
    records = EncryptedData.query.filter_by(owner_id=current_user.id)\
                                 .order_by(EncryptedData.created_at.desc()).all()
    for r in records:
        r.icon      = _icon(r.mime_type)
        r.humansize = _human_size(r.file_size)

    logs = ActivityLog.query.filter_by(user_id=current_user.id)\
                            .order_by(ActivityLog.timestamp.desc()).limit(50).all()
    return render_template('history.html', records=records, logs=logs)
