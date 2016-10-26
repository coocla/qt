#coding:utf-8
from .inventory import Inventory

__alias__ = u'库存管理'


def enable(app):
    v = Inventory(app)

def disable(app):
    pass

def check_policy(user):
    if user and user.role == 0:
        return True
    return False