#coding:utf-8
import os

DEFAULT_THEME_NAME = 'Tomorrow Night'
if os.name == 'posix':
    LOG_FILE = '/tmp/cloudtea.log'
else:
    LOG_FILE = 'D:\\cloudtea.log'