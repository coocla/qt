#coding:utf-8
from .datacenter import DataCenter

__alias__ = u'数据中心'


def enable(app):
    v = DataCenter(app)

def disable(app):
    pass

def check_policy(user):
    if user and user.role == 0:
        return True
    return False