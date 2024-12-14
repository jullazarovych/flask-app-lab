# app/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Regexp, ValidationError, Optional
from flask_wtf.file import FileAllowed
from app.users.models import User
from flask_login import current_user

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
        
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('This username is already taken. Please choose a different one.')
        
class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(),
        Length(min=4, max=14, message="This field must be between 4 and 14 characters long")
    ])
    email = StringField('Email', validators=[
        DataRequired(),
        Email(message="This field must be a valid email")
    ])
    about_me = TextAreaField('About Me', validators=[
        Length(max=500, message="This field cannot exceed 500 characters")
    ])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    password = PasswordField('New Password', validators=[
        Optional(),  # Дозволяє залишати поле порожнім
        Length(min=6, message="Password must be at least 6 characters long")
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        EqualTo('password', message="Passwords must match")
    ])
    submit = SubmitField('Update')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('This email is already registered. Please use a different one.')