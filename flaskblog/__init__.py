# access the environment variables through os module
import os

# flask module and functions
from flask import Flask

# SQLAlchemy module (ORM)
from flask_sqlalchemy import SQLAlchemy

# hashing module
from flask_bcrypt import Bcrypt

# user login module
from flask_login import LoginManager

# email module
from flask_mail import Mail

# start the server 
app = Flask(__name__)

# application secret key
app.config['SECRET_KEY'] = 'e48b6e01762d0335a47e2b9cdaa389c8'

# set location of the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

# create the database
db = SQLAlchemy(app)

# create the crypting object
bcrypt = Bcrypt(app)

# create user login manager object
login_manager = LoginManager(app)

# required by login_required decorator from flask_login module
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
 
# mail related configurations
app.config['MAIL_SERVER'] = 'smtp.office365.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')
mail = Mail(app)

# import the routes 
# should alway be inported after the app install has been created
from flaskblog import routes
