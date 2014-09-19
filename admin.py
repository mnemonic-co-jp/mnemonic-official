# coding: utf-8
# Author: Somin Kobayashi

import webapp2
import os
import jinja2
import json
import datetime
import time
import logging
import settings
import filters
import utilities

from google.appengine.api import users

from models import Entry, Tag

jinja_environment = jinja2.Environment(
  loader = jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates/admin'))
)
jinja_environment.filters.update({
  'datetime2jdate': filters.datetime2jdate,
  'datetime2string': filters.datetime2string,
})
jinja_environment.globals.update({
  'get_request': webapp2.get_request
})

class BaseHandler(webapp2.RequestHandler):
  def is_admin(self):
    user = users.get_current_user()
    if user is None:
      self.redirect(users.create_login_url(self.request.uri))
    if user is not None and user.nickname() == settings.ADMIN_USER:
      return True
    return False

  def request2params(self, request):
    try:
      date = datetime.datetime.strptime(request.get('date'), "%Y/%m/%d %H:%M:%S")
    except Exception as e:
      print e
      date = datetime.datetime.now()
    return {
      'title': request.get('title'),
      'date': utilities.jst2utc(date).replace(tzinfo=None),
      'twitter_ids': [int(id) for id in request.get('twitter_ids').splitlines()],
      'body': request.get('body'),
      'tags': request.get_all('tags'),
      'is_published': request.get('is_published') == '1'
    }

class MainHandler(BaseHandler):
  def get(self):
    if not self.is_admin():
      return
    template = jinja_environment.get_template('index.html')
    self.response.out.write(template.render())

class EntryListHandler(BaseHandler):
  def get(self):
    if not self.is_admin():
      return
    entries = Entry.get_entries()
    template = jinja_environment.get_template('entry_list.html')
    self.response.out.write(template.render({
      'entries': entries
    }))

class EditEntryHandler(BaseHandler):
  def get(self, entry_id):
    if not self.is_admin():
      return
    entry = Entry.get_entry(entry_id)
    if entry is None:
      return
    template = jinja_environment.get_template('entry_edit.html')
    self.response.out.write(template.render({
      'is_new': False,
      'entry': entry,
      'tagnames': json.dumps(Tag.get_tagnames(), ensure_ascii=False),
      'alert': None
    }))

  def post(self, entry_id):
    if not self.is_admin():
      return
    entry = Entry.update_entry(entry_id, self.request2params(self.request))
    if entry is None:
      entry = Entry.get_entry(entry_id)
      alert = {
        'type': 'danger',
        'content': u'変更できませんでした。'
      }
    else:
      alert = {
        'type': 'info',
        'content': u'変更内容を保存しました。'
      }
    template = jinja_environment.get_template('entry_edit.html')
    self.response.out.write(template.render({
      'is_new': False,
      'entry': entry,
      'tagnames': json.dumps(Tag.get_tagnames(), ensure_ascii=False),
      'alert': alert
    }))

class CreateEntryHandler(BaseHandler):
  def get(self):
    if not self.is_admin():
      return
    entry = {
      'date': datetime.datetime.now(),
      'is_published': True
    }
    template = jinja_environment.get_template('entry_edit.html')
    self.response.out.write(template.render({
      'is_new': True,
      'entry': entry,
      'tagnames': json.dumps(Tag.get_tagnames(), ensure_ascii=False),
      'alert': None
    }))

  def post(self):
    if not self.is_admin():
      return
    entry = Entry.update_entry(None, self.request2params(self.request), True)
    if entry is None:
      is_new = True
      entry = {}
      alert = {
        'type': 'danger',
        'content': u'新しい投稿を保存できませんでした。'
      }
    else:
      is_new = False
      alert = {
        'type': 'info',
        'content': u'新しい投稿を保存しました。'
      }
    template = jinja_environment.get_template('entry_edit.html')
    self.response.out.write(template.render({
      'is_new': is_new,
      'entry': entry,
      'tagnames': json.dumps(Tag.get_tagnames(), ensure_ascii=False),
      'alert': alert
    }))

class DeleteEntryHandler(BaseHandler):
  def get(self, entry_id):
    if not self.is_admin():
      return
    if not Entry.delete_entry(entry_id):
      pass # 削除失敗時の処理が必要？
    time.sleep(0.1)
    self.redirect(self.request.referer)

class ApiGetTagListHandler(BaseHandler):
  def get(self):
    tags = Tag.get_tags()
    tag_list = []
    for tag in tags:
      tag_list.append({
        'name': tag.name,
        'count': tag.count
      })
    result = {
      'tags': tag_list
    }
    self.response.headers['Content-Type'] = 'application/javascript charset=utf-8'
    self.response.out.write(json.dumps(result).decode('utf_8'))

app = webapp2.WSGIApplication([
  (r'/admin/?', MainHandler),
  (r'/admin/entry/?', EntryListHandler),
  (r'/admin/entry/(\d+)/?', EditEntryHandler),
  (r'/admin/entry/(\d+)/del/?', DeleteEntryHandler),
  (r'/admin/entry/new/?', CreateEntryHandler),
  (r'/admin/api/tags', ApiGetTagListHandler)
], debug=True)
