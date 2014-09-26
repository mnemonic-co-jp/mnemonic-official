# coding: utf-8
# Author: Somin Kobayashi

from google.appengine.ext import ndb
import datetime
import time

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
  def get_entries(cls, num=None, offset=0):
    query = cls.query(cls.is_published == True, cls.is_deleted == False).order(-cls.date)
    if num is None:
      return query.fetch()
    else:
      return query.fetch(num, offset=offset)

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
        entry.tags = sorted(list(set(value)), key=unicode.lower)
      if key == 'is_published':
        entry.is_published = value
    try:
      entry.put()
      time.sleep(0.1)
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
      time.sleep(0.1)
      Tag.update_tags(entry.tags)
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
  name_lower = ndb.ComputedProperty(lambda self: self.name.lower())
  count = ndb.IntegerProperty(default=0)

  @classmethod
  def get_tags(cls):
    return cls.query().order(cls.name_lower).fetch()

  @classmethod
  def get_tagnames(cls):
    tags = cls.get_tags()
    tagnames = []
    for t in tags:
      tagnames.append(t.name)
    return tagnames

  @classmethod
  def update_tags(cls, tag_list):
    tags = cls.get_tags()
    tagnames = []
    for t in tags:
      tagnames.append(t.name)
    for tagname in tag_list:
      if tagname not in tagnames:
        tag = cls(name=tagname)
        tag.put()
    entries = Entry.get_entries()
    tag_count_dict = {}
    for entry in entries:
      for tagname in entry.tags:
        if tag_count_dict.has_key(tagname):
          tag_count_dict[tagname] += 1
        else:
          tag_count_dict[tagname] = 1
    for key, value in tag_count_dict.items():
      tag = cls.query(cls.name == key).fetch()[0]
      tag.count = value
      tag.put()
    time.sleep(0.1)
    tags = cls.get_tags()
    for tag in tags:
      if tag.name not in tag_count_dict:
        tag.count = 0
        tag.put()
