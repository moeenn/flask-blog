from flask_wtf import FlaskForm 
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

# create and update articles
class ArticleForm(FlaskForm):
    title = StringField('Title', validators=[ DataRequired() ])
    content = TextAreaField('Content', validators=[ DataRequired() ])
    submit = SubmitField('Post Article')
