from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog.models import User
from flask_login import current_user

# main user registration form
class RegistrationForm(FlaskForm):
    name = StringField('Name', 
                           validators=[ DataRequired(), Length( min = 2, max=20 )])
    
    email = StringField( 'Email', 
                            validators=[ DataRequired(), Email() ])
    
    password = PasswordField('Password', 
                            validators=[ DataRequired(), Length(min=8) ])
    
    confirm_password = PasswordField('Confirm Password', 
                            validators=[ DataRequired(), Length(min=8), EqualTo('password') ])
    
    submit = SubmitField('Register')
    
    def validate_name(self, name):
        user = User.query.filter_by( name = name.data ).first()
        if user:
            raise ValidationError('This User Name is taken. Please try another one.')
    
    def validate_email(self, email):
        user = User.query.filter_by( email = email.data ).first()
        if user:
            raise ValidationError('This Email address has been taken. Please use another one.')


# user login form    
class LoginForm(FlaskForm):
    email = StringField( 'Email', 
                            validators=[ DataRequired(), Email() ])
    
    password = PasswordField('Password', 
                            validators=[ DataRequired(), Length(min=8) ])
        
    remember = BooleanField('Remember Me')
    
    submit = SubmitField('Login')


# account recovery form
class RecoverAccount(FlaskForm):
    email = StringField('Email', validators=[ DataRequired(), Email() ])
    submit = SubmitField('Submit')

    def validate_email(self, email):
        user = User.query.filter_by(email = email.data ).first()
        if user is None:
            raise ValidationError('There is no account with this email. You must register first.')


# form for entering the new passwords 
class RecoverAccountPassword(FlaskForm):
    password = PasswordField('Password', 
                            validators=[ DataRequired(), Length(min=8) ])
    
    confirm_password = PasswordField('Confirm Password', 
                            validators=[ DataRequired(), Length(min=8), EqualTo('password') ])

    submit = SubmitField('Update Password')  


# update profile settings form
class ProfileSettingsForm(FlaskForm):
    name = StringField('Name', 
                           validators=[ DataRequired(), Length( min = 2, max=20 )])
    
    email = StringField( 'Email', 
                            validators=[ DataRequired(), Email() ])

    image_file = FileField('Profile Picture', validators=[ FileAllowed([ 'jpg', 'png' ]) ])

    submit = SubmitField('Save Changes')
    
    def validate_name(self, name):
        if name.data != current_user.name:
            user = User.query.filter_by( name = name.data ).first()
            if user:
                raise ValidationError('This User Name is taken. Please try another one.')
    
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by( email = email.data ).first()
            if user:
                raise ValidationError('This Email address has been taken. Please use another one.')