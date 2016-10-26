# -*- coding: utf-8 -*-
import hashlib
import random
import sqlalchemy
import sqlalchemy.orm
from PyQt5 import QtSql, QtGui

from cloudtea import setting as opt


_MARKER = None
_ENGINE = None

def db_engine():
    global _MARK
    if _MARK is None:
    	db = QtSql.QSqlDatabase.addDatabase('QMYSQL')
    	db.setHostName(opt.db_host)
    	db.setDatabaseName(opt.db_name)
    	db.setUserName(opt.db_user)
    	db.setPassword(opt.db_password)
    	db.setPort(opt.db_port)
    	if not db.open():
    		QtGui.QMessageBox.critical(None, u'错误', u'数据库连接失败, (%s)' % db.lastError().text(), QtGui.QMessageBox.Yes, QtGui.QMessageBox.Yes)
    		import sys
    		sys.exit(999)
    	_MARK = QtSql.QSqlQuery()
    return _MARK

def get_engine():
    global _ENGINE
    if _ENGINE is None:
        engine_args = {
            "pool_recycle":5,
            "echo":False, 
            "convert_unicode":True
        }
        sql_connection = 'mysql+pymysql://%s:%s@%s:%s/%s?charset=utf8' % (opt.db_user, opt.db_password, opt.db_host, opt.db_port, opt.db_name)
        _ENGINE = sqlalchemy.create_engine(sql_connection, **engine_args)
        _ENGINE.connect()
    return _ENGINE
    
def get_session(autocommit=True, expire_on_commit=False):
    global _MARKER
    if _MARKER is None:
        Session = sqlalchemy.orm.sessionmaker(bind=get_engine(),
            autocommit=autocommit, 
            expire_on_commit=expire_on_commit)
        _MARKER = Session()
    return _MARKER
    
def create_table(models):
    for model in models:
        model.metadata.create_all(get_engine())
        

def query(model, session=None):
    if session is None:
        session = get_session()
    return session.query(model)
    
    
def get_random_string(length=8, allowed_chars='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'):
    return ''.join(random.choice(allowed_chars) for i in range(length))
    
class hasher(object):
    def encode(self, password):
        salt = self.salt()
        hash = self.make_hash(salt, password)
        return '%s$%s' % (salt, hash)
        
    def make_hash(self, salt, password):
        m = hashlib.md5()
        salt = salt.encode('utf-8')
        m.update(salt+password)
        return m.hexdigest()
        
    def salt(self):
        return get_random_string()
        
    def verify(self, password,  encoded):
        salt, hash = encoded.split('$')
        hash2 = self.make_hash(salt, password)
        return hash == hash2

def make_password(password):
    return hasher().encode(password)
    
def check_password(password, encoded):
    return hasher().verify(password,  encoded)
    
    
