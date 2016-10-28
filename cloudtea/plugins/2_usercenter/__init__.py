#coding:utf-8
from .user import User

__alias__ = u'店员管理'


def enable(app, user):
    v = User(app, user)

def disable(app):
    pass

def check_policy(user):
    if user and user.role == 0:
        return True
    return False