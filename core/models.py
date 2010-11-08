# -*- coding: utf-8 -*-
# core.models

from google.appengine.ext import db
from kay.auth.models import DatastoreUser

class MyUser(DatastoreUser):
	#address = db.TextProperty(u'住所', required=True)
	pass
	
