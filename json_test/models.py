# -*- coding: utf-8 -*-
# json_test.models

from google.appengine.ext import db
import kay.db
import pytz

class Tweet(db.Model):
	# author that owns this entity.
	author = kay.db.OwnerProperty()
	# basic info.
	tweet = db.TextProperty(required=True)
	created = db.DateTimeProperty(auto_now_add=True)

	@property
	def created_t(self):
		d = self.created
		_zone = pytz.timezone('Asia/Tokyo')
		return _zone.fromutc(d).strftime("%m/%d %H:%M")

	# key-list method
	# boards that belong to this entity.
	boards = db.ListProperty(db.Key)


class Board(db.Model):
	# BoardObject's name
	name = db.StringProperty()
	others = db.ListProperty(db.Key)

	@property
	def tweets(self):
		q = Tweet.gql("WHERE boards = :1 ORDER BY created DESC", self.key())
		return q.fetch(MAX_DISP_TWEETS)


