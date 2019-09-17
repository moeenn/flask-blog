import os

# We can create a configuration class so that we ca
# contain all configurations inside a configuration object
class Config:
	# application secret key. TODO: Store in environment variables
	SECRET_KEY = 'e48b6e01762d0335a47e2b9cdaa389c8'

	# set location of the database
	SQLALCHEMY_DATABASE_URI = 'sqlite:///database/site.db'

	# mail related configurations
	MAIL_SERVER = 'smtp.office365.com'
	MAIL_PORT = 587
	MAIL_USE_TLS = True
	MAIL_USERNAME = os.environ.get('EMAIL_USER')
	MAIL_PASSWORD = os.environ.get('EMAIL_PASS')
