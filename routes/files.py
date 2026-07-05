import io
import mimetypes
from datetime import datetime
from flask import Blueprint, render_template, request, flash, redirect, url_for, send_file
from flask_login import login_required, current_user
from models.models import db, StoredFile
from utils.authentication import log_activity

files_bp = Blueprint('files', __name__)

def get_file_icon(mime_type: str) -> str:
    if 'pdf'   in mime_type: return '📄'
    if 'image' in mime_type: return '🖼️'
    if 'text'  in mime_type: return '📝'
    if 'zip'   in mime_type or 'compressed' in mime_type: return '🗜️'
    if 'word'  in mime_type or 'document'   in mime_type: return '📃'
    if 'sheet' in mime_type or 'excel'      in mime_type: return '📊'
    return '📁'

def _human_size(size_bytes: int) -> str:
    for unit in ('B', 'KB', 'MB', 'GB'):
        if size_bytes < 1024:
            return f'{size_bytes:.1f} {unit}'
        size_bytes /= 1024
    return f'{size_bytes:.1f} TB'


# ── UPLOAD ────────────────────────────────────────────────────────────────────

@files_bp.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_file():
    if request.method == 'POST':
        file = request.files.get('file')

        if file and file.filename != '':
            try:
                file_bytes = file.read()
                file_size  = len(file_bytes)
                mime_type  = file.mimetype or mimetypes.guess_type(file.filename)[0] or 'application/octet-stream'

                record = StoredFile(
                    user_id=current_user.id,
                    original_filename=file.filename,
                    mime_type=mime_type,
                    file_size=file_size,
                    file_data=file_bytes
                )
                db.session.add(record)
                db.session.commit()

                log_activity(current_user.id, f'Uploaded file: {file.filename}', request.remote_addr)
                flash('File uploaded successfully!', 'success')
                return redirect(url_for('files.my_files'))
                
            except Exception as e:
                flash(f'Upload failed: {str(e)}', 'danger')
        else:
            flash('Please select a file to upload.', 'warning')

    return render_template('upload.html')


# ── MY FILES DASHBOARD ────────────────────────────────────────────────────────

@files_bp.route('/my-files')
@login_required
def my_files():
    records = StoredFile.query.filter_by(user_id=current_user.id)\
                              .order_by(StoredFile.created_at.desc()).all()
    for r in records:
        r.file_icon  = get_file_icon(r.mime_type)
        r.human_size = _human_size(r.file_size)
    return render_template('my_files.html', records=records)


# ── DOWNLOAD ──────────────────────────────────────────────────────────────────

@files_bp.route('/download/<int:file_id>')
@login_required
def download_file(file_id):
    record = StoredFile.query.filter_by(id=file_id, user_id=current_user.id).first_or_404()

    # Update stats
    record.download_count += 1
    record.last_accessed   = datetime.utcnow()
    db.session.commit()

    log_activity(current_user.id, f'Downloaded file: {record.original_filename}', request.remote_addr)

    return send_file(
        io.BytesIO(record.file_data),
        as_attachment=True,
        download_name=record.original_filename,
        mimetype=record.mime_type
    )

# ── DELETE ────────────────────────────────────────────────────────────────────

@files_bp.route('/delete/<int:file_id>', methods=['POST'])
@login_required
def delete_file(file_id):
    record = StoredFile.query.filter_by(id=file_id, user_id=current_user.id).first_or_404()
    
    filename = record.original_filename
    db.session.delete(record)
    db.session.commit()

    log_activity(current_user.id, f'Deleted file: {filename}', request.remote_addr)
    flash(f'File "{filename}" has been deleted.', 'info')
    
    return redirect(url_for('files.my_files'))
