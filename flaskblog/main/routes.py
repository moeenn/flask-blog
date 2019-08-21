from flask import Blueprint, request, render_template
from flaskblog.models import Post

main = Blueprint('main', __name__)

# define the homepage
@main.route('/')
@main.route('/home')
def home():
    # get the current page number from URL
    # format: get( argName, defaultValue, argDataType )
    page_num = request.args.get('page', 1, type=int)

    # paginate the posts, 5 posts per page
    # order is descending order i.e. newest posts first
    posts = Post.query.order_by(Post.date_posted.desc()).paginate( page = page_num, per_page = 5)
    return render_template('home.html', posts=posts)

    
# about page
@main.route('/about')
def about():
    return render_template('about.html', title='About')