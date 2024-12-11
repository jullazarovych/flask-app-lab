# app/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Regexp, ValidationError
from app.users.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(), 
        Length(min=4, max=16),
        Regexp("^[A-Za-z][A-Za-z0-9_.]*$", 
               message="Username must start with a letter and contain only letters, numbers, dots or underscores.")
    ])
    
    email = StringField('Email', validators=[
        DataRequired(), 
        Email()
    ])
    
    password = PasswordField('Password', validators=[
        DataRequired(), 
        Length(min=6)
    ])
    
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(), 
        EqualTo('password')
    ])
    
    submit = SubmitField('Register')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email is already registered.')