from flaskr.application import check_title
from flask import (Blueprint, flash, g, redirect, render_template, url_for, request)
from werkzeug.exceptions import abort
from flaskr.auth import loginrequired
from flaskr.repositories import PostRepository

bp=Blueprint("blog",__name__)

@bp.route("/")
def index():
    post_repository = PostRepository()
    posts= post_repository.get_posts()
    if posts is None:
        posts = []
    return render_template("blog/index.html",posts=posts)

def getpost(id, checkauthor=True):
    post_repository = PostRepository()
    post=post_repository.get_post(id)
    if post is None:
        abort(404, f"Post id {id} doesn't exist")
    if checkauthor and post['author_id']!=g.user['id']:
        abort(403)
    return post


@bp.route('/create',methods=('GET', 'POST'))
@loginrequired
def create():
    post_repository = PostRepository()
    if request.method=='POST':
        title=request.form['title']
        body=request.form['body']
        error=None
        if not title:
            error='Title is required'
        if error is not None:
            flash(error)
        else:
            user_id = g.user['id']
            post_repository.add_post(title, body, user_id)
            return redirect(url_for('blog.index'))
    return render_template('blog/create.html')


@bp.route("/<int:id>/update", methods=('GET', "POST"))
@loginrequired
def update(id):
    post_repository = PostRepository()
    post=getpost(id)
    if request.method=='POST':
        title=request.form['title']
        body=request.form['body']
        error=check_title(title)
        if error is not None:
            flash(error)
        else:
            post_repository.update_post(title, body, id)
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)

@bp.route('/<int:id>/delete',methods=('POST',))
@loginrequired
def delete(id):
    post_repository = PostRepository()
    getpost(id)
    post_repository.delete_post(id)
    return redirect(url_for('blog.index'))
