from cloudtea.db import utils

from cloudtea.db import models
a=b'admin'
b=b'123'
c=a+b
print(c)
 
user = utils.query(models.Users)
user.update({"password":'JNqNVThH$ee849bc514b7cd324c5f9e44b2a7b7fd'})