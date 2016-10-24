#coding:utf-8
from .sale import Sale

__alias__ = u'活动配置'


def enable(app):
    v = Sale(app)

def disable(app):
    pass

def check_policy(user):
    if user and user.role == 0:
        return True
    return False