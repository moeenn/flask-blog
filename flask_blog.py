# flask module and functions
from flask import Flask, render_template, flash, redirect, request

# SQLAlchemy module (ORM)
from flask_sqlalchemy import SQLAlchemy

# date time module
from datetime import datetime

# import forms
from forms import RegistrationForm, LoginForm, RecoverAccount

# start the server 
app = Flask('__name__')

# application secret key
app.config['SECRET_KEY'] = 'e48b6e01762d0335a47e2b9cdaa389c8'

# set location of the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

# create the database
db = SQLAlchemy(app)

# users table
class User(db.Model):
    id = db.Column( db.Integer, primary_key = True )
    name = db.Column( db.String(20), unique = True, nullable = False )
    email = db.Column( db.String(120), unique = True, nullable = False )
    image_file = db.Column( db.String(20), nullable = False, default = 'default.jpg' )
    password = db.Column( db.String(60), nullable = False )
    posts = db.relationship('Post', backref = 'author', lazy = True )
    
    def __repr__(self):
        return f"User('{self.name}', '{self.email}', '{self.image_file}')"

# table for posts
class Post(db.Model):
    id = db.Column( db.Integer, primary_key = True )
    title = db.Column( db.String(200), nullable = False )
    date_posted = db.Column( db.DateTime, nullable = False, default = datetime.utcnow )
    content = db.Column( db.Text, nullable = False )
    user_id = db.Column( db.Integer, db.ForeignKey('user.id'), nullable = False )
    
    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


# dummy data
posts = [
    {
      'author': 'Carl Sagan', 
      'title': 'Pale Blue Dot', 
      'content': 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam',
      'date':'June 30, 1990'
    },
    {
      'author': 'Neil Tyson', 
      'title': 'String Theory', 
      'content': 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam',
      'date':'February 15, 2003'
    },
    {
      'author': 'Michio Kaku', 
      'title': 'Soap Bubble Universe', 
      'content': 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam',
      'date':'November 27, 2009'
    },
    {
      'author': 'Max Tedmark', 
      'title': 'AI - The Last Invention of Man', 
      'content': 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam',
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
    form = RegistrationForm()
    
    # check if the inputs validate successfully
    if form.validate_on_submit():
        flash(f'Registration Successful. Welcome to Flask Blog', 'positive')
        # redirect to home page
        return redirect('home')

    return render_template('register.html', title='Register', form=form)

# file: flask_blog.py
# login page
@app.route('/login', methods=[ 'GET', 'POST'])
def login():
    form = LoginForm()
    
    # check if the form data validated successfully
    if form.validate_on_submit():
        # dummy login data
        admin_account = { 'email':'admin@flaskblog.com', 'password':'password' }
        
        if form.email.data == admin_account['email'] and form.password.data == admin_account['password']:
            # display the message to the user
            flash(f'Login Successful: {form.email.data}', 'positive')
            # redirect to the home page
            #return redirect(url_for('home'))
            return redirect('home')

        else:
            flash(f'Login Failed', 'negative')
        
        
    return render_template('login.html', title='Login', form=form)


# account recovery page
@app.route('/recover_account', methods=[ 'GET', 'POST'])
def recover_account():
    form = RecoverAccount()
    
    if form.validate_on_submit():
        flash(f"""Your request for account recovery has been submitted.
               If the provided email address matches our records an email
               will be sent to the email address with the link to reset the password.""",
                'positive')
        
        return redirect('home')
    
    return render_template('recover_account.html', title='Recover Account', form=form)


if __name__ == '__main__':
    # start the app in debug mode
    app.run(debug=True)
