# -*- coding: utf-8 -*-
import datetime
import logging

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, VARCHAR, DateTime, Text, Boolean, Float
from sqlalchemy import ForeignKey, schema, Table
from sqlalchemy.orm import relationship, backref

from cloudtea.db.utils import create_table, make_password, check_password, get_session

logger = logging.getLogger(__name__)
Base = declarative_base()

def NOW():
    return datetime.datetime.now()
    
def ORDERS():
    return "P%s" % NOW().strftime('%Y%m%d%H%M%S')
    
class Model(object):
    __table_args__ = {
    "mysql_engine":"InnoDB", 
    "mysql_charset":"utf8", 
    "extend_existing":True,
    }
    created_at = Column(DateTime, default=NOW)


    def __init__(self, **kw):
        for k,v in kw.items():
            setattr(self, k, v)

    def commit(self):
        try:
            session = get_session()
            session.add(self)
            session.flush()
            return self.id, None
        except Exception as e:
            logger.error(e, exc_info=True)
            return self, e

    def delete(self, session):
        try:
            session.delete(self)
            session.flush()
            return None, None
        except Exception as e:
            logger.error(e, exc_info=True)
            return self, e


class Users(Base, Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(VARCHAR(50), unique=True)
    username = Column(VARCHAR(50), unique=True, index=True)
    password = Column(VARCHAR(100))
    phone = Column(VARCHAR(100))
    age = Column(Integer)
    sex = Column(VARCHAR(50))
    role = Column(Integer, default=2)  #0-超级管理员 1-收银员 2-服务员

    @property
    def role_display(self):
        if self.role == 0:
            return u"超级管理员"
        elif self.role == 1:
            return u"收银员"
        else:
            return u"服务员"


class Members(Base, Model):
    __tablename__ = 'members'
    id = Column(Integer, primary_key=True)
    name = Column(VARCHAR(50))
    vip_id = Column(VARCHAR(100))
    phone = Column(VARCHAR(100))
    amount = Column(Integer)

class Rooms(Base, Model):
    __tablename__ = 'rooms'
    id = Column(Integer, primary_key=True)
    name = Column(VARCHAR(50))
    inused = Column(Boolean, default=False)
    vip_price = Column(Integer)
    common_price = Column(Integer)
    capacity = Column(Integer)
    opened_at = Column(DateTime)
    
class Category(Base, Model):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    name = Column(VARCHAR(50))
    inventory = relationship('Inventory')
    
class Inventory(Base, Model):
    __tablename__ = 'inventory'
    id = Column(Integer, primary_key=True)
    name = Column(VARCHAR(50))             # 品名
    specifications = Column(VARCHAR(100))  # 规格
    number = Column(Integer)            # 数量
    meter = Column(Integer)             # 计量方式   0 重量  1 袋
    price = Column(Integer)             # 价格
    suttle = Column(Integer)            # 净重
    category_id = Column(Integer, ForeignKey('category.id'), nullable=False)


class UserInventory(Base, Model):
    __tablename__ = 'user_inventory'
    id = Column(Integer, primary_key=True)
    surplus = Column(Integer)
    user_id = Column(Integer, ForeignKey('users.id'))
    inventory_id = Column(Integer, ForeignKey('inventory.id'))


def check_and_create_super_admin():
    session = get_session()
    super_admin = session.query(Users).filter_by(id=1).first()
    if not super_admin:
        super_admin = Users(name=u"超级管理员", username="admin", password=make_password('123456'.encode('utf-8')), age=24, sex=u'女', role=0, id=1)
        session.add(super_admin)
        session.flush()

create_table((Users, Members, Rooms, Category, Inventory, UserInventory))
check_and_create_super_admin()
