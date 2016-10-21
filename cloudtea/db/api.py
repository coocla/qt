#coding:utf-8
from cloudtea.db.models import *
from cloudtea.db.utils import get_engine,  get_session, query


def get_user(username, session=None):
    return query(Users).filter_by(username=username).first()

def list_room():
    return query(Rooms).all()
    

if __name__ == '__main__':
	get_user('admin')
	