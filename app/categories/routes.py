from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.categories import bp
from app.categories.forms import CategoryForm
from app.models import Category

@bp.route('/')
@login_required
def index():
    categories = Category.query.filter_by(user_id=current_user.id).order_by(Category.name).all()
    return render_template('categories/index.html', title='Category Management',
                         categories=categories)

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = CategoryForm()
    if form.validate_on_submit():
        category = Category(
            name=form.name.data,
            user_id=current_user.id
        )
        db.session.add(category)
        db.session.commit()
        flash('Category has been created successfully!', 'success')
        return redirect(url_for('categories.index'))
    
    return render_template('categories/form.html', title='Add Category',
                         form=form, category=None)

@bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    category = Category.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    form = CategoryForm(obj=category)
    
    if form.validate_on_submit():
        category.name = form.name.data
        db.session.commit()
        flash('Category has been updated successfully!', 'success')
        return redirect(url_for('categories.index'))
    
    return render_template('categories/form.html', title='Edit Category',
                         form=form, category=category)

@bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    category = Category.query.filter_by(id=id, user_id=current_user.id).first_or_404()
    
    # Check if category has accounts
    if category.accounts:
        flash('Cannot delete this category because it is being used by accounts.', 'danger')
        return redirect(url_for('categories.index'))
    
    db.session.delete(category)
    db.session.commit()
    flash('Category has been deleted successfully!', 'success')
    return redirect(url_for('categories.index')) 