from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length


class ShareForm(FlaskForm):
    expires_in = SelectField('Expiration Time',
                             coerce=int,
                             choices=[
                                 (1, '1 hour'),
                                 (24, '24 hours'),
                                 (72, '3 days'),
                                 (168, '7 days'),
                                 (720, '30 days')
                             ],
                             validators=[DataRequired(message='Please select expiration time.')])

    access_pin = StringField('Access PIN',
                             validators=[
                                 DataRequired(message='Please enter access PIN.'),
                                 Length(min=4, max=6, message='PIN must be between 4 and 6 characters.')
                             ])

    submit = SubmitField('Create Share Link')


class AccessForm(FlaskForm):
    access_pin = StringField('Access PIN',
                             validators=[
                                 DataRequired(message='Please enter access PIN.'),
                                 Length(min=4, max=6, message='PIN must be between 4 and 6 characters.')
                             ])

    submit = SubmitField('Access')