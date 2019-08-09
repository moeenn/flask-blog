# start the server 
from flask import Flask, render_template
app = Flask('__name__')

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
@app.route('/register')
def register():
    return render_template('register.html')

# login page
@app.route('/login')
def login():
    return render_template('login.html')


if __name__ == '__main__':
    # start the app in debug mode
    app.run(debug=True)
