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
  views = ndb.IntegerProperty(default=0)
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
      date=datetime.datetime.now(),
      twitter_ids=[
        480238014119956480,
        480238687272202240,
        480239039262363648,
        480239438878892032
      ],
      body=u'あああああ/nいいいいい',
      tags=[
        u'ほげほげ',
        u'ふがふが',
        u'ほげほげ'
      ]
    )
    entry.put()

  @classmethod
  def increment_views(cls, entry_id):
    entry = cls.get_entry(entry_id)
    if entry is not None:
      entry.views += 1
      entry.put()
