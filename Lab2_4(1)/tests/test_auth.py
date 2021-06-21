from flaskr.auth import delete_user
from logging import error
from flaskr.application import *
from flaskr.repositories import UserRepository, PostRepository
from flaskr.auth import *

def test_register_no_username():
    error = check_password('', "password", 123)
    assert error == 'Username is required'

def test_register_user_existing():
    class TestRepository:

        def get_user(self, username):
            return ""

    error = check_password('username', "password", TestRepository())
    assert error == "User username is already registered"


def test_register_no_password():
    error = check_password('123', '', 123)
    assert error == 'Password is required'  

def test_register():
    user_repository = UserRepository()
    error = check_password('username', "password", user_repository)
    id=user_repository.get_user('username')
    user_repository.delete_user(id['id'])
    assert error == None


def test_login_incorect_username():
    error=None
    user=None
    error=check_login(user, '123')
    assert error=='Incorrect username'

def test_login_incorect_password():
    error=None
    from werkzeug.security import check_password_hash, generate_password_hash
    user={}
    user['password']=generate_password_hash('1234')
    error=check_login(user, '123')
    assert error=='Incorrect password'

def test_login():
    error=None
    from werkzeug.security import check_password_hash, generate_password_hash
    user={}
    user['password']=generate_password_hash('123')
    error=check_login(user, '123')
    assert error==None




