#coding:utf-8
from .system import System

__alias__ = u'系统设置'


def enable(app, user):
    v = System(app, user)

def disable(app):
    pass

def check_policy(user):
    if user and user.role == 0:
        return True
    return False