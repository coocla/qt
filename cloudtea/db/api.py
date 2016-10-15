#coding:utf-8
from cloudtea.db import utils

def get_user(username):
	query = utils.db_engine()
	if '&' in username or ';' in username:
		return None
	query.exec_('select id, name, role from users where username="%(username)s"' % locals())
	if query.first():
		user = {}
		user["id"] = query.value(0)
		user["name"] = query.value(1)
		user["role"] = query.value(2)
		print user
		return user
	return None


if __name__ == '__main__':
	get_user('admin')
	