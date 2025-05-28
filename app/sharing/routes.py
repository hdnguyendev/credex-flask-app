from flask import render_template, redirect, url_for, flash, request, session
from flask_login import login_required, current_user
from app import db
from app.sharing import bp
from app.sharing.forms import ShareForm, AccessForm
from app.models import Account, SharedLink
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

@bp.route('/')
@login_required
def index():
    shared_links = SharedLink.query.filter_by(user_id=current_user.id).all()
    return render_template('sharing/index.html', title='Share Management', shared_links=shared_links)

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    account_id = request.args.get('account_id', type=int)
    if not account_id:
        flash('Account not found.', 'danger')
        return redirect(url_for('accounts.index'))
    
    account = Account.query.filter_by(id=account_id, user_id=current_user.id).first_or_404()
    form = ShareForm()
    
    if form.validate_on_submit():
        try:
            logger.debug(f"Creating shared link for account {account_id}")
            
            # Calculate expiration time based on selection
            hours = form.expires_in.data
            expires_at = datetime.utcnow() + timedelta(hours=hours)
            
            # Create new share link with PIN from form
            shared_link = SharedLink(
                account_id=account.id,
                user_id=current_user.id,
                access_pin=form.access_pin.data,
                expires_at=expires_at
            )
            
            logger.debug(f"Created shared link with token {shared_link.token} and PIN {shared_link.access_pin}")
            
            db.session.add(shared_link)
            db.session.commit()
            
            flash('Share link has been created successfully!', 'success')
            return redirect(url_for('sharing.index'))
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error creating shared link: {str(e)}", exc_info=True)
            flash('An error occurred while creating the share link. Please try again.', 'danger')
    elif form.errors:
        logger.error(f"Form validation errors: {form.errors}")
    
    return render_template('sharing/form.html', title='Share Account', form=form, account=account)

@bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    shared_link = SharedLink.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    db.session.delete(shared_link)
    db.session.commit()
    flash('Share link has been deleted.', 'success')
    return redirect(url_for('sharing.index'))

@bp.route('/access/<token>', methods=['GET', 'POST'])
def access(token):
    shared_link = SharedLink.query.filter_by(token=token).first_or_404()
    
    # Check expiration
    if shared_link.expires_at < datetime.utcnow():
        flash('Share link has expired.', 'danger')
        return redirect(url_for('main.index'))
    
    form = AccessForm()
    if form.validate_on_submit():
        logger.debug(f"Access attempt for token {token} with PIN {form.access_pin.data}")
        if form.access_pin.data == shared_link.access_pin:
            # Increment access count
            shared_link.increment_access_count()
            logger.debug(f"Access granted for token {token}")
            
            # Save verification status in session
            session[f'verified_{token}'] = True
            
            # Redirect to account information page
            return redirect(url_for('sharing.view', token=token))
        else:
            logger.warning(f"Invalid PIN attempt for token {token}")
            flash('Invalid PIN.', 'danger')
    
    # Only show PIN input form, don't show account information
    return render_template('sharing/access.html', 
                         title='Enter PIN',
                         form=form)

@bp.route('/view/<token>')
def view(token):
    shared_link = SharedLink.query.filter_by(token=token).first_or_404()
    
    # Check expiration
    if shared_link.expires_at < datetime.utcnow():
        flash('Share link has expired.', 'danger')
        return redirect(url_for('main.index'))
    
    # Check PIN verification
    if not session.get(f'verified_{token}'):
        flash('Please enter PIN to access account information.', 'warning')
        return redirect(url_for('sharing.access', token=token))
    
    return render_template('sharing/view.html', 
                         title='Account Information',
                         shared_link=shared_link) 