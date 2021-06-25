import functools
import asyncio

from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.repositories import UserRepository, PostRepository, UserStatusRepository
from flaskr.application import *
from just_config.configuration import Configuration
import logging

cfg = Configuration('flask_app')

bp=Blueprint('auth', __name__, url_prefix='/auth')
user_repository = UserRepository()
user_status_repository = UserStatusRepository()
post_repository = PostRepository()

@bp.route('/register', methods=('GET','POST'))
def register():
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']
        status = request.form['status']
        error, user_id = check_password(username, password, user_repository)
        logging.info(f'creating user with id: {user_id}')

        if not error:
            user_status_repository.add_status(user_id, status)
            return redirect(url_for('auth.login'))
        flash(error)
    return render_template('auth/register.html')

@bp.route('/login', methods=('GET','POST'))
def login():
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']
        error=None
        user= user_repository.get_user(username)
        error=check_login(user, password)
        if error is None:
            session.clear()
            session['user_id']=user['id']
            return redirect(url_for('index'))
        flash(error)
    return render_template('auth/login.html')

@bp.route('/adminlogin', methods=('GET','POST'))
def adminlogin():
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']
        error=check_login_admin(username, password, cfg)
        if error is None:
            session.clear()
            session['admin']=True
            return redirect(url_for('auth.admin'))
        flash(error)
    return render_template('auth/login.html')

@bp.before_app_request
def loadloggedinuser():
    user_id=session.get('user_id')
    if user_id is None:
        g.user=None
    else:
        g.user=(user_repository.get_user_by_id(user_id))
    if session.get('admin'):
        g.admin=True
    else:
        g.admin=None

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

def loginrequired(view):
    @functools.wraps(view)
    def wrappedview(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrappedview

def adminrequired(view):
    @functools.wraps(view)
    def wrappedview(**kwargs):
        if g.admin is None:
            return redirect(url_for('auth.adminlogin'))
        return view(**kwargs)
    return wrappedview

@bp.route('/admin', methods=('GET','POST'))
@adminrequired
def admin():
    return render_template('blog/admin.html')

def user_logic(message=''):
    users = user_repository.get_users()
    return render_template('auth/records.html', records = users, url='delete_user', message=message)


@bp.route('/users', methods=['GET'])
def users():
    message = ''
    if 'msg' in g.__dict__:
        message = g.msg
        g.msg = ''
    return user_logic(message)

@bp.route('/posts',  methods=['GET'])
def posts():
    posts = post_repository.get_posts()
    return render_template('auth/records.html', records = posts, url='delete_post')


@bp.route('/statuses',  methods=['GET'])
def show_statuses():
    statuses = user_status_repository.get_statuses()
    return render_template('auth/records.html', records = statuses, url='delete_status')

@bp.route('/delete_status/<int:id>/', methods=['POST'])
@adminrequired
def delete_status(id):
    return 'Статус удалить нельзя, удалите пользователя'



@bp.route('/delete_post/<int:id>/', methods=['POST'])
@adminrequired
def delete_post(id):
    delete_post_logic(id)
    return redirect(url_for('auth.posts'))


def delete_post_logic(id):
    post_repository.delete_post(id)

async def delete_user_logic(id):
    posts=post_repository.get_posts(id)
    for post in posts:
        delete_post_logic(post['id'])
    status=user_status_repository.get_status(id)
    user_status_repository.delete_record(status['id'])
    user_repository.delete_user(id)

async def delete_user_async(id):
    task = asyncio.create_task(delete_user_logic(id))
    await task

@bp.route('/delete_user/<int:id>/', methods=['POST'])
@adminrequired
def delete_user(id):
    asyncio.run(delete_user_async(id))
    g.msg = 'Пользователь удаляется в асинхронном режиме, попробуйте обновить страницу через 5 минут'
    return redirect(url_for('auth.users'))