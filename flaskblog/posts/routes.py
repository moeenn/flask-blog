from flask import Blueprint, render_template, url_for, flash, redirect, request, abort
from flaskblog.models import Post
from flask_login import login_required, current_user
from flaskblog.posts.forms import ArticleForm
from flaskblog import db

# this will replace the @app route decorator
posts = Blueprint('posts', __name__)

# article page
# accept the id from the url
@posts.route('/article/<int:post_id>')
def article(post_id):
    # if the requested post doesn't exist, return 404
    post = Post.query.get_or_404(post_id)
    return render_template('article.html', title=post.title, post=post) 


# create new article
@posts.route('/article/new_article', methods=[ 'GET', 'POST'])
@login_required
def new_article():
    form = ArticleForm()

    if form.validate_on_submit():
        post = Post( title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()

        flash('The Article has been posted Successfully', 'positive')
        return redirect( url_for('posts.article', post_id=post.id) )

    return render_template('create_update_article.html', title='New Article', form=form)


# update article
@posts.route('/article/<int:post_id>/update', methods=['GET', 'POST'])
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
            return redirect( url_for('posts.article', post_id=post.id) )

        elif request.method == 'GET':
            # set the placeholders for the input fields
            form.title.data = post.title
            form.content.data = post.content

    return render_template('create_update_article.html', title='Update Article', form=form)

# delete posts
@posts.route('/article/<int:post_id>/delete')
@login_required
def delete_article(post_id):
    post = Post.query.get_or_404(post_id)

    if post.author != current_user:
        abort(403)
    else:
        db.session.delete(post)
        db.session.commit()
        flash('Article has been deleted Successfully', 'positive')
        return redirect( url_for('users.profile', username=current_user.name) )