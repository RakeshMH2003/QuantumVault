from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()


class User(db.Model, UserMixin):
    """Platform user — can be from any company."""
    __tablename__ = 'users'
    id            = db.Column(db.Integer, primary_key=True)
    username      = db.Column(db.String(50),  unique=True, nullable=False)
    email         = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role          = db.Column(db.String(20),  nullable=False, default='user')  # 'user' | 'admin'
    company       = db.Column(db.String(100), nullable=True)
    is_active     = db.Column(db.Boolean, default=True)
    created_at    = db.Column(db.DateTime, default=datetime.utcnow)
    last_login    = db.Column(db.DateTime, nullable=True)

    logs           = db.relationship('ActivityLog',  backref='user', lazy='dynamic', cascade='all, delete-orphan')
    encryptions    = db.relationship('EncryptedData', foreign_keys='EncryptedData.owner_id',
                                     backref='owner', lazy='dynamic', cascade='all, delete-orphan')


class EncryptedData(db.Model):
    """
    Encrypted payload vault.
    Owner encrypts → generates QRC code.
    Any authenticated user can decrypt using that code (cross-company sharing).
    """
    __tablename__ = 'encrypted_data'
    id                = db.Column(db.Integer, primary_key=True)
    owner_id          = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # QRC Code — shared between companies
    qrc_code          = db.Column(db.String(20), unique=True, nullable=False, index=True)

    # Payload metadata
    original_filename = db.Column(db.String(255), nullable=False)
    mime_type         = db.Column(db.String(100), nullable=False, default='application/octet-stream')
    file_size         = db.Column(db.Integer, default=0)
    description       = db.Column(db.String(500), nullable=True)  # optional note from sender

    # Encrypted binary — stored directly in PostgreSQL
    encrypted_blob    = db.Column(db.LargeBinary, nullable=False)

    # Stats
    is_active         = db.Column(db.Boolean, default=True)   # owner can revoke
    decrypt_count     = db.Column(db.Integer, default=0)
    last_decrypted_at = db.Column(db.DateTime, nullable=True)
    last_decrypted_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    created_at        = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at        = db.Column(db.DateTime, nullable=True)  # optional expiry


class ActivityLog(db.Model):
    """Full audit trail — every encrypt/decrypt/login is recorded."""
    __tablename__ = 'activity_log'
    id         = db.Column(db.Integer, primary_key=True)
    user_id    = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    action     = db.Column(db.String(50),  nullable=False)   # 'ENCRYPT' | 'DECRYPT' | 'LOGIN' | 'LOGOUT' | etc.
    detail     = db.Column(db.String(500), nullable=True)
    qrc_code   = db.Column(db.String(20),  nullable=True)    # associated QRC if relevant
    ip_address = db.Column(db.String(45),  nullable=True)
    status     = db.Column(db.String(20),  default='SUCCESS') # 'SUCCESS' | 'FAILED'
    timestamp  = db.Column(db.DateTime,   default=datetime.utcnow)
