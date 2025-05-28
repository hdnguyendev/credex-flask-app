from datetime import datetime
from app import db
import logging

logger = logging.getLogger(__name__)

class Category(db.Model):
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Relationships
    user = db.relationship('User', back_populates='categories')
    accounts = db.relationship('Account', back_populates='category', cascade='all, delete-orphan')
    
    @staticmethod
    def create_default_categories(user_id):
        """Create default categories for a new user."""
        default_categories = [
            {'name': 'Social Media', 'description': 'Social media accounts'},
            {'name': 'Email', 'description': 'Email accounts'},
            {'name': 'Banking', 'description': 'Banking and financial accounts'},
            {'name': 'Shopping', 'description': 'Online shopping accounts'},
            {'name': 'Work', 'description': 'Work-related accounts'},
            {'name': 'Other', 'description': 'Other accounts'}
        ]
        
        try:
            for category_data in default_categories:
                category = Category(
                    name=category_data['name'],
                    description=category_data['description'],
                    user_id=user_id
                )
                db.session.add(category)
            
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'user_id': self.user_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Category {self.name}>' 