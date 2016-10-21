#coding:utf-8
from .room import ROOM

__alias__ = u'房间管理'


def enable(app):
    r = ROOM(app)

def disable(app):
    pass

def check_policy(user):
    if user and user.role == 0:
        return True
    return False