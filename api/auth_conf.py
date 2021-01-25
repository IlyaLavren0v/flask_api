from user import User 
from werkzeug.security import safe_str_cmp


def authenticate(username, password):
    user = User.search_username(username)
    if user  and safe_str_cmp(user.password , password):
        return user 


def identity(data):
    uid = data['identity']
    return User.search_id(uid)