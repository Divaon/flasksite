def check_password(username, password, user_repository):
    error=None
    if not username:
        error='Username is required'
    elif not password:
        error = 'Password is required'
    elif user_repository.get_user(username) is not None:
        error = f"User {username} is already registered"
    if error is None:
        user_repository.add_user(username, password)
    return error

def check_login(user, password):
    error=None
    from werkzeug.security import check_password_hash
    if user is None:
        error='Incorrect username'
    elif not check_password_hash(user['password'],password):
        error='Incorrect password'
    return error