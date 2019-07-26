from reward_app.db import AppUser, db
import hashlib


def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()


def check_auth(username, password):
    user = AppUser.query.filter_by(username=username).first()
    if user is None:
        return False
    return hash_password(password) == user.password


def create_user(username, password):
    user = AppUser()
    user.username = username
    user.password = hash_password(password)
    db.session.add(user)
    db.session.commit()
    return user
