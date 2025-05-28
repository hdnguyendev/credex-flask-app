from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class CategoryForm(FlaskForm):
    name = StringField('Category Name', validators=[
        DataRequired(message='Please enter category name.'),
        Length(max=100, message='Category name cannot exceed 100 characters.')
    ])
    submit = SubmitField('Save') 