# for generating random file names for renaming uploaded files
import secrets

# for obtaining the extension of uploaded files
import os

# resize images with Pillow
from PIL import Image

# routes specific imports
from flask import render_template, url_for, flash, redirect, request, abort

# import the objects from __init__.py
from flaskblog import app, db, bcrypt, mail

# import forms
from flaskblog.forms import RegistrationForm, LoginForm, RecoverAccount, ProfileSettingsForm, ArticleForm, RecoverAccountPassword

# import the models for tables
from flaskblog.models import User, Post

# user login 
from flask_login import login_user, current_user, logout_user, login_required

# message class from the flask_mail module
from flask_mail import Message

# define the homepage
@app.route('/')
@app.route('/home')
def home():
    # get the current page number from URL
    # format: get( argName, defaultValue, argDataType )
    page_num = request.args.get('page', 1, type=int)

    # paginate the posts, 5 posts per page
    # order is descending order i.e. newest posts first
    posts = Post.query.order_by(Post.date_posted.desc()).paginate( page = page_num, per_page = 5)
    return render_template('home.html', posts=posts)
    
    
# about page
@app.route('/about')
def about():
    return render_template('about.html', title='About')


# registration page
@app.route('/register', methods=[ 'GET', 'POST'])
def register():
    # redirect to home if user already logged in
    if current_user.is_authenticated:
        return redirect( url_for('home') )
    
    form = RegistrationForm()
    
    # check if the inputs validate successfully
    if form.validate_on_submit():
        # calculate hash of the entered password
        hashed_password = bcrypt.generate_password_hash( form.password.data ).decode('utf-8')
        
        # create the user in the DB
        user = User( name = form.name.data, email = form.email.data, password = hashed_password )
        
        # write the new user to the DB
        db.session.add( user )
        db.session.commit()
        
        # tell user that the account has been created
        flash(f'Your Account has been created. Welcome to Flask Blog', 'positive')

        # redirect to login page
        return redirect( url_for('login') )

    return render_template('register.html', title='Register', form=form)


# login page
@app.route('/login', methods=[ 'GET', 'POST'])
def login():
    # redirect to home is user is already logged in
    if current_user.is_authenticated:
        return redirect( url_for('home') )
    
    form = LoginForm()
    
    # check if the form data validated successfully
    if form.validate_on_submit():
        user = User.query.filter_by( email = form.email.data ).first()
        
        if user and bcrypt.check_password_hash( user.password, form.password.data ):
            login_user( user, remember = form.remember.data )
            flash(f'Login Successful.', 'positive')
            return redirect( url_for('profile', username=user.name) )
            
        else:
            flash(f'Login Unsuccessful. Please check email and password', 'negative')            

    return render_template('login.html', title='Login', form=form)


# log out the user
@app.route('/logout')
def logout():
    logout_user()
    return redirect( url_for('home') )

# send the password reset email with link to reset the password
# the reset token will be part of the URL
def send_reset_email(user):
    # generate the token for the provided user
    token = user.get_reset_token()
    # message headers i.e. Subject, sender and the recipients
    msg = Message('Password Reset Request', sender='noreply@demo.com', recipients=[user.email])

    # _external=True is an argument for the url_for() function
    # it means that the generated URL will be absolute rather than relative (defaut)
    msg.body = f'''To reset your Password, visit the following link:
{url_for('recover_account_password', token=token, _external=True)}

If you did not request to change your password, simply ignore this email and no changes will be made.
'''
    # send the actual email
    mail.send(msg)

# account recovery page
@app.route('/recover_account', methods=[ 'GET', 'POST'])
def recover_account():
    # redirect to home if user already logged in
    if current_user.is_authenticated:
        return redirect( url_for('home') )
    
    form = RecoverAccount()
    
    if form.validate_on_submit():
        user = User.query.filter_by( email = form.email.data ).first()
        send_reset_email(user)

        flash(f'An email has been sent with the instructions to reset the Password.', 'info')
        return redirect( url_for('login') )
    
    return render_template('recover_account.html', title='Recover Account', form=form)


# set the new passwords after recovery
# get the reset token from the user as argument
@app.route('/recover_account/update_password/<string:token>', methods=['GET', 'POST'] )
def recover_account_password(token):
    # redirect to home if user already logged in
    if current_user.is_authenticated:
        return redirect( url_for('home') )

    # verify the token. If valid, user is returned, else None is returned
    user = User.verify_reset_token(token)
    if user is None:
        flash('The Token is invalid or has expired.', 'negative')
        return redirect( url_for('recover_account') )
    else:
        form = RecoverAccountPassword()

        if form.validate_on_submit():
            hashed_password = bcrypt.generate_password_hash( form.password.data ).decode('utf-8')
            user.password = hashed_password
            db.session.commit()
            flash('Your Password has been Updated Successfully. You can now log in with the new Password', 'positive')
            return redirect('login')

    return render_template('recover_account_password.html', title='Reset Password', form=form)


# profile page
@app.route('/profile/<string:username>')
def profile(username):
    user = User.query.filter_by(name=username).first_or_404()

    # get the page number
    page_num = request.args.get('page', 1, type=int )

    # user posts, latest first i.e. descending order, paginated 
    posts = Post.query.filter_by( user_id=user.id ).order_by(Post.date_posted.desc()).paginate( page=page_num, per_page=5 )

    image_file = url_for('static', filename=f'profile_pictures/{user.image_file}')
    return render_template('profile.html', title='Profile', image_file=image_file , posts=posts, user=user)


# save pictures. NOT a route function
def save_image( form_picture ):
    # need to set random hex as file name to avoid conflicts
    random_hex = secrets.token_hex(8)

    # get the extension of uploaded file
    # splitext() returns filename and fileext
    # underscore means we ignore the first value returned 
    _, file_ext = os.path.splitext( form_picture.filename )

    # new file name for uploaded file
    final_file_name = random_hex + file_ext

    # address for saving file
    final_file_path = os.path.join( app.root_path, 'static/profile_pictures', final_file_name )

    # resize the image (using Pillow module)
    output_size = ( 250, 250 )
    i = Image.open(form_picture)
    i = i.crop(( 0, 0, min(i.size), min(i.size) ))
    i.thumbnail(output_size)

    # save the image the the final path (save method from Pillow)
    i.save(final_file_path)

    # delete the old profile picture
    old_file_path = os.path.join( app.root_path, 'static/profile_pictures', current_user.image_file )
    os.remove(old_file_path)

    # return the new file name for saving in the DB
    return final_file_name

# profile settings page
@app.route('/profile/settings', methods=[ 'GET', 'POST'])
@login_required
def profile_settings():
    form = ProfileSettingsForm()

    if form.validate_on_submit():
        if form.image_file.data:
            new_file_name = save_image( form.image_file.data )
            # update current user's profile pic in DB
            current_user.image_file = new_file_name

        current_user.name = form.name.data
        current_user.email = form.email.data
        # save the settings to db
        db.session.commit()
        flash('Settings Updated Successfully', 'positive')
        return redirect( url_for('profile') )

    # set the placeholders for the input fields
    elif request.method == 'GET':
        form.name.data = current_user.name
        form.email.data = current_user.email

    image_file = url_for('static', filename=f'profile_pictures/{current_user.image_file}')
    return render_template('profile_settings.html', title='Profile Settings', image_file=image_file, form=form)


# article page
# accept the id from the url
@app.route('/article/<int:post_id>')
def article(post_id):
    # if the requested post doesn't exist, return 404
    post = Post.query.get_or_404(post_id)
    return render_template('article.html', title=post.title, post=post) 


# create new article
@app.route('/article/new_article', methods=[ 'GET', 'POST'])
@login_required
def new_article():
    form = ArticleForm()

    if form.validate_on_submit():
        post = Post( title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()

        flash('The Article has been posted Successfully', 'positive')
        return redirect( url_for('article', post_id=post.id) )

    return render_template('create_update_article.html', title='New Article', form=form)


# update article
@app.route('/article/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_article(post_id):
    post = Post.query.get_or_404(post_id)

    if post.user_id != current_user.id:
        # imported from Flask. 403 = Access Denied
        abort(403)
    else:
        form = ArticleForm()

        if form.validate_on_submit():
            post.title = form.title.data
            post.content = form.content.data
            db.session.commit()

            flash('Article Updated Successfully', 'positive')
            return redirect( url_for('article', post_id=post.id) )

        elif request.method == 'GET':
            # set the placeholders for the input fields
            form.title.data = post.title
            form.content.data = post.content

    return render_template('create_update_article.html', title='Update Article', form=form)

# delete posts
@app.route('/article/<int:post_id>/delete')
@login_required
def delete_article(post_id):
    post = Post.query.get_or_404(post_id)

    if post.author != current_user:
        abort(403)
    else:
        db.session.delete(post)
        db.session.commit()
        flash('Article has been deleted Successfully', 'positive')
        return redirect( url_for('profile', user_id=current_user.id) )