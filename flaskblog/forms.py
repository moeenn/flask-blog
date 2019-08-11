# file: forms.py
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo

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
