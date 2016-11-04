#coding:utf-8
from .wechat import WeChat

__alias__ = u'微信营销'


def enable(app, user):
    v = WeChat(app, user)

def disable(app):
    pass

def check_policy(user):
    if user and user.role == 0:
        return True
    return False