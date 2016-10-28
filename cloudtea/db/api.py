#coding:utf-8
from sqlalchemy import or_

from cloudtea.db.models import *
from cloudtea.db import utils
from cloudtea.db.utils import get_engine,  get_session, query


########## User Model ##########
def get_user(username, session=None):
    try:
        int(username)
        return query(Users).filter_by(id=username).first()
    except:
        return query(Users).filter_by(username=username).first()

def list_user():
    return query(Users).filter(Users.id!=1).all()

def verify_username(text):
    return query(Users).filter_by(username=text).first()

def search_user(text):
    return query(Users).filter(or_(\
        Users.name.like('%%%s%%' % text),\
        Users.username.like('%%%s%%' % text),\
        Users.phone.like('%%%s%%' % text))).all()

def create_user(user, name, username, password, sex, age, phone, role=3):
    u = Users(name=name, username=username, password=utils.make_password(password.encode('utf-8')), role=role, sex=sex, age=age, phone=phone)
    return u.commit()

########## Room Model ##########
def get_room(pk, session=None):
    return query(Rooms, session=session).filter_by(id=pk).first()

def list_room():
    return query(Rooms).all()

def search_room(text):
    return query(Rooms).filter(Rooms.name.like('%%%s%%' % text)).all()

def create_room(user, name, vp, cp, capacity):
    room = Rooms(name=name, vip_price=vp, common_price=cp, capacity=capacity)
    return room.commit()

########## VIP Model ##########
def get_vip(pk, session=None):
    return query(Members, session=session).filter_by(id=pk).first()

def list_vip():
    return query(Members).all()
    
if __name__ == '__main__':
	get_user('admin')
	