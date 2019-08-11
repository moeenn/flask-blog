# flask module and functions
from flask import Flask

# SQLAlchemy module (ORM)
from flask_sqlalchemy import SQLAlchemy

# start the server 
app = Flask(__name__)

# application secret key
app.config['SECRET_KEY'] = 'e48b6e01762d0335a47e2b9cdaa389c8'

# set location of the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

# create the database
db = SQLAlchemy(app)
 
# inport the routes 
# should alway be inported after the app install has been created
from flaskblog import routes
