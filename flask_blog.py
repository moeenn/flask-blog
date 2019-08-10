from flask import Flask, render_template, flash, redirect

# import forms
from forms import RegistrationForm, LoginForm

# start the server 
app = Flask('__name__')

# application secret key
app.config['SECRET_KEY'] = 'e48b6e01762d0335a47e2b9cdaa389c8'

# dummy data
posts = [
    {
      'author': 'Carl Sagan', 
      'title': 'Pale Blue Dot', 
      'content': 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam'
    },
    {
      'author': 'Neil Tyson', 
      'title': 'String Theory', 
      'content': 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam'
    },
    {
      'author': 'Michio Kaku', 
      'title': 'Soap Bubble Universe', 
      'content': 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam'
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
        # display the message to the user
        flash(f'Login Successful: {form.email.data}', 'positive')
        
        # redirect to the home page
        #return redirect(url_for('home'))
        return redirect('home')
        
    return render_template('login.html', title='Login', form=form)


if __name__ == '__main__':
    # start the app in debug mode
    app.run(debug=True)
