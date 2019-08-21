import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_login import current_user
from flask_mail import Message
from flaskblog import mail

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
    final_file_path = os.path.join( current_app.root_path, 'static/profile_pictures', final_file_name )

    # resize the image (using Pillow module)
    output_size = ( 250, 250 )
    i = Image.open(form_picture)
    i = i.crop(( 0, 0, min(i.size), min(i.size) ))
    i.thumbnail(output_size)

    # save the image the the final path (save method from Pillow)
    i.save(final_file_path)

    # delete the old profile picture
    old_file_path = os.path.join( current_app.root_path, 'static/profile_pictures', current_user.image_file )
    os.remove(old_file_path)

    # return the new file name for saving in the DB
    return final_file_name


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
{url_for('users.recover_account_password', token=token, _external=True)}

If you did not request to change your password, simply ignore this email and no changes will be made.
'''
    # send the actual email
    mail.send(msg)