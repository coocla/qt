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
    return query(Members, session=session).filter(or_(Members.id==pk, Members.vip_id==pk)).first()

def list_vip():
    return query(Members).all()
    
def search_vip(text):
    return query(Members).filter(or_(Members.name.like('%%%s%%' % text), Members.vip_id.like('%%%s%%' % text), \
        Members.phone.like('%%%s%%' % text))).all()

def create_vip(user, name, vip_id, amount, phone):
    vip = Members(name=name, vip_id=vip_id, amount=amount, phone=phone)
    return vip.commit()

########## Inventory Model ##########
def get_inventory(pk, session=None):
    return query(Inventory, session=session).filter_by(id=pk).first()

def list_inventory():
    return query(Inventory).all()

def search_inventory(text):
    return query(Inventory).filter(Inventory.name.like('%%%s%%' % text)).all()

def create_inventory(user, name, specifications, number, meter, price, suttle, category_id):
    inventory = Inventory(name=name, specifications=specifications, number=number, meter=meter, \
        price=price, suttle=suttle, category_id=category_id)
    return inventory.commit()

########## Inventory Category Model ##########
def get_category(pk, session=None):
    return query(Category, session=session).filter(or_(Category.id==pk, Category.name==pk)).first()

def list_category():
    return query(Category).all()

def search_category(text):
    return query(Category).filter(Category.name.like('%%%s%%' % text)).all()

def create_category(user, name):
    category = Category(name=name)
    return category.commit()





if __name__ == '__main__':
	get_user('admin')
	