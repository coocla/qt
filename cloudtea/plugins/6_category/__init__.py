#coding:utf-8
from .category import CategoryManage

__alias__ = u'货品分类'


def enable(app, user):
    v = CategoryManage(app, user)

def disable(app):
    pass

def check_policy(user):
    if user and user.role == 0:
        return True
    return False