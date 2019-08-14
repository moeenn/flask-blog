# routes specific imports
from flask import render_template, url_for, flash, redirect, request

# import the objects from __init__.py
from flaskblog import app, db, bcrypt

# import forms
from flaskblog.forms import RegistrationForm, LoginForm, RecoverAccount

# import the models for tables
from flaskblog.models import User, Post

# user login 
from flask_login import login_user, current_user, logout_user, login_required


# dummy data
posts = [
    {
      'author': 'Carl Sagan', 
      'title': 'Pale Blue Dot', 
      'content': 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam ...',
      'date':'June 30, 1990'
    },
    {
      'author': 'Neil Tyson', 
      'title': 'String Theory', 
      'content': 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam ...',
      'date':'February 15, 2003'
    },
    {
      'author': 'Michio Kaku', 
      'title': 'Soap Bubble Universe', 
      'content': 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam ...',
      'date':'November 27, 2009'
    },
    {
      'author': 'Max Tedmark', 
      'title': 'AI - The Last Invention of Man', 
      'content': 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam ...',
      'date':'April 10, 2016'
    }    
]


# define the homepage
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', posts=posts)
    
    
# about page
@app.route('/about')
def about():
    return render_template('about.html', title='About')


# registration page
@app.route('/register', methods=[ 'GET', 'POST'])
def register():
    # redirect to home if user already logged in
    if current_user.is_authenticated:
        return redirect( url_for('home') )
    
    form = RegistrationForm()
    
    # check if the inputs validate successfully
    if form.validate_on_submit():
        # calculate hash of the entered password
        hashed_password = bcrypt.generate_password_hash( form.password.data ).decode('utf-8')
        
        # create the user in the DB
        user = User( name = form.name.data, email = form.email.data, password = hashed_password )
        
        # write the new user to the DB
        db.session.add( user )
        db.session.commit()
        
        # tell user that the account has been created
        flash(f'Your Account has been created. Welcome to Flask Blog', 'positive')

        # redirect to login page
        return redirect( url_for('login') )

    return render_template('register.html', title='Register', form=form)


# login page
@app.route('/login', methods=[ 'GET', 'POST'])
def login():
    # redirect to home is user is already logged in
    if current_user.is_authenticated:
        return redirect( url_for('home') )
    
    form = LoginForm()
    
    # check if the form data validated successfully
    if form.validate_on_submit():
        user = User.query.filter_by( email = form.email.data ).first()
        
        if user and bcrypt.check_password_hash( user.password, form.password.data ):
            login_user( user, remember = form.remember.data )
            flash(f'Login Successful.', 'positive')
            return redirect(next_page) if next_page else redirect( url_for('home') )
            
        else:
            flash(f'Login Unsuccessful. Please check email and password', 'negative')            

    return render_template('login.html', title='Login', form=form)


# log out the user
@app.route('/logout')
def logout():
    logout_user()
    return redirect( url_for('home') )


# account recovery page
@app.route('/recover_account', methods=[ 'GET', 'POST'])
def recover_account():
    # redirect to home if user already logged in
    if current_user.is_authenticated:
        return redirect( url_for('home') )
    
    form = RecoverAccount()
    
    if form.validate_on_submit():
        flash(f'Your request for account recovery has been submitted.', 'positive')
        return redirect( url_for('home') )
    
    return render_template('recover_account.html', title='Recover Account', form=form)


# user profile page
@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', title='Profile', posts=posts )


# article page
@app.route('/article')
def article():
    return render_template('article.html', title='Article' ) 
