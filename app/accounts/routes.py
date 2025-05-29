from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, current_app
from flask_login import login_required, current_user
from app import db
from app.accounts import bp
from app.accounts.forms import AccountForm, SearchForm
from app.models import Account, Category
import logging

logger = logging.getLogger(__name__)

@bp.route('/')
@login_required
def index():
    form = SearchForm()
    form.category_id.choices = [(c.id, c.name) for c in Category.query.filter_by(user_id=current_user.id).all()]
    form.category_id.choices.insert(0, (0, 'All'))
    
    # Populate form with GET parameters
    if request.method == 'GET':
        form.search.data = request.args.get('search', '')
        form.category_id.data = request.args.get('category_id', type=int)
    
    query = Account.query.filter_by(user_id=current_user.id)
    
    # Apply search filter
    if form.search.data:
        query = query.filter(Account.name.ilike(f'%{form.search.data}%'))
    
    # Apply category filter
    if form.category_id.data and form.category_id.data != 0:
        query = query.filter_by(category_id=form.category_id.data)
    
    accounts = query.order_by(Account.name).all()
    return render_template('accounts/index.html', title='Account Management',
                         accounts=accounts, form=form)

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = AccountForm()
    form.category_id.choices = [(c.id, c.name) for c in Category.query.filter_by(user_id=current_user.id).all()]
    
    if form.validate_on_submit():
        try:
            logger.debug(f"Form data: {form.data}")
            logger.debug(f"Password from form: {form.password.data}")
            
            if not form.password.data:
                flash('Password is required', 'error')
                return render_template('accounts/form.html', form=form, title='Create Account')
            

            # Create account
            account = Account(
                name=form.name.data,
                username=form.username.data,
                email=form.email.data,
                notes=form.notes.data,
                url=form.url.data,
                user_id=current_user.id,
                category_id=form.category_id.data
            )
            
            # Set password using the new method
            account.set_password(form.password.data)
            
            # Verify password was set
            if not account.password:
                raise ValueError("Password hashing failed")
            
            db.session.add(account)
            db.session.commit()
            flash('Account created successfully!', 'success')
            return redirect(url_for('accounts.index'))
        except Exception as e:
            logger.error(f"Error creating account: {str(e)}", exc_info=True)
            db.session.rollback()
            flash(f'Error creating account: {str(e)}', 'error')
    else:
        logger.debug(f"Form validation errors: {form.errors}")
    
    return render_template('accounts/form.html', form=form, title='Create Account')

@bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    account = Account.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    form = AccountForm(obj=account)
    form.category_id.choices = [(c.id, c.name) for c in Category.query.filter_by(user_id=current_user.id).all()]
    
    if form.validate_on_submit():
        account.name = form.name.data
        account.username = form.username.data
        account.email = form.email.data
        account.notes = form.notes.data
        account.url = form.url.data
        account.category_id = form.category_id.data
        
        # Only update password if a new one is provided
        if form.password.data:
            account.set_password(form.password.data)
        
        db.session.commit()
        flash('Account updated successfully!', 'success')
        return redirect(url_for('accounts.index'))
    
    return render_template('accounts/form.html', 
                         title='Edit Account', 
                         form=form,
                         account=account)

@bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    account = Account.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    db.session.delete(account)
    db.session.commit()
    flash('Account deleted successfully!', 'success')
    return redirect(url_for('accounts.index'))

@bp.route('/<int:id>/password')
@login_required
def get_password(id):
    account = Account.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    return jsonify({ 'password': account.get_password() })