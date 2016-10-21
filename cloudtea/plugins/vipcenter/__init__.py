#coding:utf-8
from .vip import VIP

__alias__ = u'会员中心'


def enable(app):
    pass

def disable(app):
    pass

def check_policy(user):
    if user and user.role == 0:
        return True
    return False