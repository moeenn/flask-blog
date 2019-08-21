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

# configuration class
from flaskblog.config import Config

# create the database
db = SQLAlchemy()

# create the crypting object
bcrypt = Bcrypt()

# create user login manager object
login_manager = LoginManager()

# required by login_required decorator from flask_login module
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

# mail for password recovery 
mail = Mail()

# allow for creation of different instances of the app e.g. for testing, staging and production
def create_app(config_class=Config):
	# start the server 
	app = Flask(__name__)

	# load the configuration from config object
	app.config.from_object(config_class)

	db.init_app(app)
	bcrypt.init_app(app)
	login_manager.init_app(app)
	mail.init_app(app)

	# import the blueprint objects from the sub-package routes
	# should alway be inported after the app install has been create 
	from flaskblog.users.routes import users
	from flaskblog.posts.routes import posts
	from flaskblog.main.routes import main

	# register the imported blueprints with the app
	app.register_blueprint(users)
	app.register_blueprint(posts)
	app.register_blueprint(main)

	return app