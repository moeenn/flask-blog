from flaskblog import db, login_manager, app
from datetime import datetime
from flask_login import UserMixin

# create auto-expiring tokens (for password reset emails)
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

# set up the user sessions
@login_manager.user_loader
def load_user( user_id ):
    return User.query.get( int(user_id) )


# users table
class User(db.Model, UserMixin):
    id = db.Column( db.Integer, primary_key = True )
    name = db.Column( db.String(20), unique = True, nullable = False )
    email = db.Column( db.String(120), unique = True, nullable = False )
    image_file = db.Column( db.String(20), nullable = False, default = 'avatar.png' )
    password = db.Column( db.String(60), nullable = False )
    posts = db.relationship('Post', backref = 'author', lazy = True )
    
    # generate the token for reseting the password through email
    def get_reset_token(self, expires_seconds = 1800 ):
    	# create the serializer object
    	s = Serializer(app.config['SECRET_KEY'], expires_seconds)
    	# return the token
    	return s.dumps({ 'user_id': self.id }).decode('utf-8')

    # verify the token. User will not be logged-in when using this method, therefore no self
    @staticmethod
    def verify_reset_token(token):
    	s = Serializer(app.config['SECRET_KEY'])
    	try:
    		# try to decode the token. loads() returns a dictionary, get the user_id key
    		user_id = s.loads(token)['user_id']
    	except:
    		# if error, return Nothing
    		return None
    	else:
    		# if no error, return the user with the user_id
    		return User.query.get(user_id)


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
 