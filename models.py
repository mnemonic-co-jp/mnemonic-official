# coding: utf-8
# Author: Somin Kobayashi

from google.appengine.ext import ndb
import datetime

class BaseModel(ndb.Model):
	created_at = ndb.DateTimeProperty(auto_now_add=True)
	updated_at = ndb.DateTimeProperty(auto_now=True)

class Entry(BaseModel):
	title = ndb.StringProperty()
	date = ndb.DateTimeProperty()
	twitter_ids = ndb.IntegerProperty(repeated=True)
	body = ndb.TextProperty()
	tags = ndb.StringProperty(repeated=True)
	is_published = ndb.BooleanProperty(default=False)
	is_deleted = ndb.BooleanProperty(default=False)

	@classmethod
	def get_entries(cls):
		return cls.query().order(-cls.date)

	@classmethod
	def get_entry(cls, entry_id):
		return cls.get_by_id(int(entry_id))

	@classmethod
	def create_entry(cls):
		# stab
		entry = cls(
			title='hogehoge',
			date=datetime.datetime.now()
		)
		entry.put()