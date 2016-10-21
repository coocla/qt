#coding:utf-8
import logging
import logging.config

from .consts import LOG_FILE

dict_config = { 
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': "[%(levelname)s] "
                      "[%(module)s %(funcName)s %(lineno)d] "
                      ": %(message)s",
        },  
    },  
    'handlers': {
        'debug': {
            'formatter': 'standard',
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },  
        'release': {
            'formatter': 'standard',
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': LOG_FILE,
            'mode': 'w',
        }   
    },  
    'loggers': {
        'cloudtea': {
            'handlers': ['debug'],
            'level': logging.DEBUG,
            'propagate': True
        },  
    }   
}

def logger_config():
    logging.config.dictConfig(dict_config)
