from flaskr.auth import delete_user
from logging import error
from flaskr.application import *
from flaskr.repositories import UserRepository, PostRepository
from flaskr.auth import *
from just_config.configuration import Configuration
cfg = Configuration('flask_app')

def test_register_no_username():
    error , id= check_password('', "password", 123)
    assert error == 'Username is required' and id==None

def test_register_user_existing():
    class TestRepository:

        def get_user(self, username):
            return ""

    error,id = check_password('username', "password", TestRepository())
    assert error == "User username is already registered" and id==None


def test_register_no_password():
    error ,id= check_password('123', '', 123)
    assert error == 'Password is required'  and id==None

def test_register():
    user_repository = UserRepository()
    error,id1 = check_password('username', "password", user_repository)
    id=user_repository.get_user('username')
    user_repository.delete_user(id['id'])
    assert error == None and id1==id['id']


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

def test_login_admin():
    error=None
    error=check_login_admin(cfg['ADMIN_USERNAME'], cfg['ADMIN_PASSWORD'], cfg)
    assert error==None

def test_login_admin_incorrect_username():
    error=None
    error=check_login_admin('rehre', cfg['ADMIN_PASSWORD'], cfg)
    assert error=='Incorrect username'

def test_login_admin_incorrect_password():
    error=None
    error=check_login_admin(cfg['ADMIN_USERNAME'], 'pasword', cfg)
    assert error=='Incorrect password'

def test_check_title_none():
    error=check_title('')
    assert error=='Title is required. '

def test_check_title():
    error=check_title('jgvhueg')
    assert error==None

def test_add_user():
        user_repository = UserRepository()
        user_repository.add_user('King', 'King')
        t=user_repository.get_user('King')
        user_repository.delete_user(t['id'])
        assert t['username']=='King'

def test_get_user_None():
        user_repository = UserRepository()
        user_repository.add_user('King', 'King')
        t=user_repository.get_user('King')
        user_repository.delete_user(t['id'])
        t=user_repository.get_user('King')
        assert t==None

def test_get_users():
        user_repository = UserRepository()
        t=user_repository.get_users()
        print(type(t))
        assert type(t)==list

def test_delete_user():
        user_repository = UserRepository()
        user_repository.add_user('King', 'King')
        t=user_repository.get_user('King')
        user_repository.delete_user(t['id'])
        t=user_repository.get_user('King')
        assert t==None

