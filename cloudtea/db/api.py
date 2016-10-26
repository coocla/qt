#coding:utf-8
from cloudtea.db.models import *
from cloudtea.db.utils import get_engine,  get_session, query


def get_user(username, session=None):
    return query(Users).filter_by(username=username).first()

def get_room(pk, session=None):
    return query(Rooms, session=session).filter_by(id=pk).first()

def list_room():
    return query(Rooms).all()

def create_room(user, name, vp, cp, capacity):
    room = Rooms(name=name, vip_price=vp, common_price=cp, capacity=capacity)
    return room.commit()

    

if __name__ == '__main__':
	get_user('admin')
	