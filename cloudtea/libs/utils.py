#coding:utf-8
import random
import hashlib

def get_random_string(length=8, allowed_chars='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'):
    return ''.join(random.choice(allowed_chars) for i in range(length))

class hasher(object):
    def encode(self, password):
        salt = self.salt()
        hash = self.make_hash(salt, password)
        return '%s$%s' % (salt, hash)
        
    def make_hash(self, salt, password):
        return hashlib.md5('%s$%s' % (salt, password)).hexdigest()
        
    def salt(self):
        return get_random_string()
        
    def verify(self, encoded,  password):
        salt, hash = encoded.split('$')
        hash2 = self.make_hash(salt, password)
        return hash == hash2

def make_password(raw_passwd):
    return hasher().encode(raw_passwd)

def check_password(encoded, passwd):
    return hasher().verify(encoded,  password)