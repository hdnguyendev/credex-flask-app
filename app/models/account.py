from app import db
from datetime import datetime
from app.services.encryption import EncryptionService
from app.config import ENCRYPTION_KEY
import logging

logger = logging.getLogger(__name__)

class Account(db.Model):
    __tablename__ = 'accounts'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120))  # Added email field
    password = db.Column(db.String(500), nullable=False)  # Increased length for encrypted password
    notes = db.Column(db.Text)
    url = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    
    # Relationships
    user = db.relationship('User', back_populates='accounts')
    category = db.relationship('Category', back_populates='accounts')
    shared_links = db.relationship('SharedLink', back_populates='account', cascade='all, delete-orphan')
    
    def __init__(self, **kwargs):
        super(Account, self).__init__(**kwargs)
        self._encryption_service = EncryptionService(ENCRYPTION_KEY)
        
        # Ensure password is encrypted before saving
        if 'password' in kwargs and kwargs['password']:
            logger.debug(f"Encrypting password for new account {kwargs.get('name', 'Unknown')}")
            encrypted = self._encryption_service.encrypt(kwargs['password'])
            if not encrypted:
                logger.error("Failed to encrypt password during account creation")
                raise ValueError("Failed to encrypt password")
            self.password = encrypted
            logger.debug("Password encrypted successfully")
    
    @property
    def encryption_service(self):
        if not hasattr(self, '_encryption_service'):
            self._encryption_service = EncryptionService(ENCRYPTION_KEY)
        return self._encryption_service
    
    def get_password(self) -> str:
        """Get the decrypted password."""
        try:
            if not self.password:
                logger.warning(f"No password found for account {self.name}")
                return None
                
            logger.debug(f"Attempting to decrypt password for account {self.name}")
            
            # Decrypt password
            decrypted = self.encryption_service.decrypt(self.password)
            if not decrypted:
                logger.error(f"Failed to decrypt password for account {self.name}")
                return None
                
            logger.debug(f"Successfully decrypted password for account {self.name}")
            return decrypted
            
        except Exception as e:
            logger.error(f"Error decrypting password for account {self.name}: {str(e)}", exc_info=True)
            return None
    
    def set_password(self, password):
        """Set encrypted password."""
        if not password:
            raise ValueError("Password cannot be empty")
            
        # Encrypt password
        encrypted = self.encryption_service.encrypt(password)
        if not encrypted:
            logger.error("Failed to encrypt password during update")
            raise ValueError("Failed to encrypt password")
            
        self.password = encrypted
        logger.debug("Password updated and encrypted successfully")
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'username': self.username,
            'email': self.email,
            'password': self.get_password(),
            'notes': self.notes,
            'url': self.url,
            'category_id': self.category_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Account {self.name}>' 