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
  is_published = ndb.BooleanProperty(default=True)
  is_deleted = ndb.BooleanProperty(default=False)

  @classmethod
  def get_entries(cls):
    return cls.query(cls.is_published == True, cls.is_deleted == False).order(-cls.date).fetch()

  @classmethod
  def get_all_entries(cls):
    return cls.query(cls.is_deleted == False).order(-cls.date).fetch()

  @classmethod
  def get_entry(cls, entry_id):
    return cls.get_by_id(int(entry_id))

  @classmethod
  def update_entry(cls, entry_id, params, is_new=False):
    if is_new:
      entry = cls(
        title='',
        date=datetime.datetime.now(),
        twitter_ids=[],
        body='',
        tags=[],
        is_published=True
      )
    else:
      entry = cls.get_by_id(int(entry_id))
    for key, value in params.items():
      if key == 'title':
        entry.title = value
      if key == 'date':
        entry.date = value
      if key == 'twitter_ids':
        entry.twitter_ids = value
      if key == 'body':
        entry.body = value
      if key == 'tags':
        entry.tags = value
      if key == 'is_published':
        entry.is_published = value
    try:
      entry.put()
      Tag.update_tags(entry.tags)
      return entry
    except:
      return None

  @classmethod
  def delete_entry(cls, entry_id):
    entry = cls.get_by_id(int(entry_id))
    entry.is_deleted = True
    try:
      entry.put()
      return True
    except:
      return False

  @classmethod
  def increment_views(cls, entry_id):
    entry = cls.get_entry(entry_id)
    if entry is not None:
      entry.views += 1
      entry.put()

class Tag(BaseModel):
  name = ndb.StringProperty()
  count = ndb.IntegerProperty(default=0)

  @classmethod
  def get_tags(cls):
    return cls.query().fetch()

  @classmethod
  def get_tagnames(cls):
    tags = cls.query().fetch()
    tagnames = []
    for t in tags:
      tagnames.append(t.name)
    return tagnames

  @classmethod
  def update_tags(cls, tag_list):
    tags = cls.query().fetch()
    tagnames = []
    for t in tags:
      tagnames.append(t.name)
    temp = []
    for tagname in tag_list:
      if tagname not in tagnames and tagname not in temp:
        tag = cls(name=tagname, count=1)
        tag.put()
        temp.append(tagname)
