from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user, logout_user, login_required
from flaskblog.users.forms import (RegistrationForm, LoginForm, RecoverAccount, 
                                RecoverAccountPassword, ProfileSettingsForm)
from flaskblog import db, bcrypt
from flaskblog.models import User, Post
from flaskblog.users.utils import save_image, send_reset_email

# this object will replace the app decorator for defining routes
users = Blueprint('users', __name__)

# registration page
@users.route('/register', methods=[ 'GET', 'POST'])
def register():
    # redirect to home if user already logged in
    if current_user.is_authenticated:
        return redirect( url_for('main.home') )
    
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
        return redirect( url_for('users.login') )

    return render_template('register.html', title='Register', form=form)


# login page
@users.route('/login', methods=[ 'GET', 'POST'])
def login():
    # redirect to home is user is already logged in
    if current_user.is_authenticated:
        return redirect( url_for('main.home') )
    
    form = LoginForm()
    
    # check if the form data validated successfully
    if form.validate_on_submit():
        user = User.query.filter_by( email = form.email.data ).first()
        
        if user and bcrypt.check_password_hash( user.password, form.password.data ):
            login_user( user, remember = form.remember.data )
            flash(f'Login Successful.', 'positive')
            return redirect( url_for('users.profile', username=user.name) )
            
        else:
            flash(f'Login Unsuccessful. Please check email and password', 'negative')            

    return render_template('login.html', title='Login', form=form)


# log out the user
@users.route('/logout')
def logout():
    logout_user()
    return redirect( url_for('main.home') )


# account recovery page
@users.route('/recover_account', methods=[ 'GET', 'POST'])
def recover_account():
    # redirect to home if user already logged in
    if current_user.is_authenticated:
        return redirect( url_for('main.home') )
    
    form = RecoverAccount()
    
    if form.validate_on_submit():
        user = User.query.filter_by( email = form.email.data ).first()
        send_reset_email(user)

        flash(f'An email has been sent with the instructions to reset the Password.', 'info')
        return redirect( url_for('users.login') )
    
    return render_template('recover_account.html', title='Recover Account', form=form)


# set the new passwords after recovery
# get the reset token from the user as argument
@users.route('/recover_account/update_password/<string:token>', methods=['GET', 'POST'] )
def recover_account_password(token):
    # redirect to home if user already logged in
    if current_user.is_authenticated:
        return redirect( url_for('main.home') )

    # verify the token. If valid, user is returned, else None is returned
    user = User.verify_reset_token(token)
    if user is None:
        flash('The Token is invalid or has expired.', 'negative')
        return redirect( url_for('users.recover_account') )
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
@users.route('/profile/<string:username>')
def profile(username):
    user = User.query.filter_by(name=username).first_or_404()

    # get the page number
    page_num = request.args.get('page', 1, type=int )

    # user posts, latest first i.e. descending order, paginated 
    posts = Post.query.filter_by( user_id=user.id ).order_by(Post.date_posted.desc()).paginate( page=page_num, per_page=5 )

    image_file = url_for('static', filename=f'profile_pictures/{user.image_file}')
    return render_template('profile.html', title='Profile', image_file=image_file , posts=posts, user=user)


# profile settings page
@users.route('/profile/settings', methods=[ 'GET', 'POST'])
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
        return redirect( url_for('users.profile', username=current_user.name) )

    # set the placeholders for the input fields
    elif request.method == 'GET':
        form.name.data = current_user.name
        form.email.data = current_user.email

    image_file = url_for('static', filename=f'profile_pictures/{current_user.image_file}')
    return render_template('profile_settings.html', title='Profile Settings', image_file=image_file, form=form)