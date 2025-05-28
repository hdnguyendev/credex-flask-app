from app import db
from datetime import datetime
from cryptography.fernet import Fernet

class EncryptionKey(db.Model):
    __tablename__ = 'encryption_keys'
    
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    
    @staticmethod
    def get_active_key():
        """Get the active encryption key."""
        key = EncryptionKey.query.filter_by(is_active=True).first()
        if not key:
            # Generate new key if none exists
            key = EncryptionKey(key=Fernet.generate_key().decode())
            db.session.add(key)
            db.session.commit()
        return key.key
    
    @staticmethod
    def rotate_key():
        """Create a new encryption key and mark the old one as inactive."""
        # Create new key
        new_key = EncryptionKey(key=Fernet.generate_key().decode())
        db.session.add(new_key)
        
        # Mark old key as inactive
        old_key = EncryptionKey.query.filter_by(is_active=True).first()
        if old_key:
            old_key.is_active = False
        
        db.session.commit()
        return new_key.key 