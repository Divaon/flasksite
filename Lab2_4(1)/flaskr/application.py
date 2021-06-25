def check_password(username, password, user_repository):
    error=None
    user_id = None
    if not username:
        error='Username is required'
    elif not password:
        error = 'Password is required'
    elif user_repository.get_user(username) is not None:
        error = f"User {username} is already registered"
    if error is None:
        user_id = user_repository.add_user(username, password)
    return error, user_id

def check_login(user, password):
    error=None
    from werkzeug.security import check_password_hash
    if user is None:
        error='Incorrect username'
    elif not check_password_hash(user['password'],password):
        error='Incorrect password'
    return error


def check_login_admin(username, password, cfg):
    error=None
    if username != cfg['ADMIN_USERNAME']:
        error='Incorrect username'
    elif password != cfg['ADMIN_PASSWORD']:
        error='Incorrect password'
    return error

def check_title(title):
    if not title:
        return 'Title is required. '
    else:
        return None


