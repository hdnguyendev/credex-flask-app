from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Optional, URL, Email, ValidationError
from app.models import Category

class AccountForm(FlaskForm):
    name = StringField('Title', validators=[DataRequired(), Length(min=1, max=100)])
    username = StringField('Username', validators=[DataRequired(), Length(min=1, max=100)])
    email = StringField('Email', validators=[Optional(), Email(), Length(max=120)])
    password = PasswordField('Password', validators=[Optional()])
    url = StringField('URL', validators=[Optional(), URL(), Length(max=200)])
    notes = TextAreaField('Notes', validators=[Optional(), Length(max=500)])
    category_id = SelectField('Category', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Save')

    def __init__(self, *args, **kwargs):
        super(AccountForm, self).__init__(*args, **kwargs)
        self.category_id.choices = [(c.id, c.name) for c in Category.query.order_by('name')]
        
        # If editing an existing account, make password optional and set current password
        if 'obj' in kwargs and kwargs['obj'] is not None:
            self.password.validators = [Optional()]
            # Set the current password in the form
            current_password = kwargs['obj'].get_password()
            if current_password:
                self.password.data = current_password
        else:
            self.password.validators = [DataRequired()]

class SearchForm(FlaskForm):
    search = StringField('Search')
    category_id = SelectField('Category', coerce=int)
    submit = SubmitField('Search') 