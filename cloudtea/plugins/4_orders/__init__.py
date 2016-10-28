#coding:utf-8
from .order import Order

__alias__ = u'活动配置'


def enable(app, user):
    v = Order(app, user)

def disable(app):
    pass

def check_policy(user):
    if user and user.role == 0:
        return True
    return False