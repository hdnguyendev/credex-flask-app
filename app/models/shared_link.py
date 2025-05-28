from app import db
from datetime import datetime, timedelta
import secrets

class SharedLink(db.Model):
    __tablename__ = 'shared_links'
    
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(64), unique=True, nullable=False)
    access_pin = db.Column(db.String(6), nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    access_count = db.Column(db.Integer, nullable=False, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', back_populates='shared_links')
    account = db.relationship('Account', back_populates='shared_links')
    
    def __init__(self, *args, **kwargs):
        super(SharedLink, self).__init__(*args, **kwargs)
        self.token = secrets.token_urlsafe(16)  # Giảm độ dài token xuống 16 ký tự
        if 'access_pin' not in kwargs:
            self.access_pin = ''.join(secrets.choice('0123456789') for _ in range(6))
    
    @property
    def is_expired(self) -> bool:
        """Check if the shared link has expired."""
        return datetime.utcnow() > self.expires_at
    
    @property
    def is_access_limit_reached(self) -> bool:
        """Check if the access limit has been reached."""
        if self.max_access_count is None:
            return False
        return self.access_count >= self.max_access_count
    
    def increment_access_count(self):
        """Increment the access count."""
        self.access_count += 1
        db.session.commit()
    
    @staticmethod
    def create(account_id: int, user_id: int, duration_hours: int = 24, max_access_count: int = None):
        """Create a new shared link."""
        expires_at = datetime.utcnow() + timedelta(hours=duration_hours)
        return SharedLink(
            account_id=account_id,
            user_id=user_id,
            expires_at=expires_at,
            max_access_count=max_access_count
        )
    
    def __repr__(self):
        return f'<SharedLink {self.token}>' 