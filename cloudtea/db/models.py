#coding:utf-8

class User(object):
    def __init__(self, user):
        for k,v in user.iteritems():
            setattr(self, k, v)