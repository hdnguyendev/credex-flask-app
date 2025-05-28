from flask import render_template
from flask_login import login_required, current_user
from app.main import bp
from app.models import Account, Category

@bp.route('/')
@bp.route('/index')
@login_required
def index():
    # Get some statistics for the dashboard
    total_accounts = Account.query.filter_by(user_id=current_user.id).count()
    total_categories = Category.query.filter_by(user_id=current_user.id).count()
    
    # Get recent accounts
    recent_accounts = Account.query.filter_by(user_id=current_user.id)\
        .order_by(Account.created_at.desc())\
        .limit(5)\
        .all()
    
    return render_template('main/index.html',
                         title='Dashboard',
                         total_accounts=total_accounts,
                         total_categories=total_categories,
                         recent_accounts=recent_accounts) 