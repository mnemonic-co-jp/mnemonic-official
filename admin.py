# coding: utf-8
# Author: Somin Kobayashi

import webapp2
import os
import jinja2
import json
import datetime
import time
import logging
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
    template = jinja_environment.get_template('index.html')
    self.response.out.write(template.render())

class EntryListHandler(BaseHandler):
  def get(self):
    entries = Entry.get_all_entries()
    template = jinja_environment.get_template('entry_list.html')
    self.response.out.write(template.render({
      'entries': entries,
      'status': self.request.get('status', None)
    }))

class EditEntryHandler(BaseHandler):
  def get(self, entry_id):
    entry = Entry.get_entry(entry_id)
    if entry is None:
      return
    template = jinja_environment.get_template('entry_edit.html')
    self.response.out.write(template.render({
      'is_new': not not self.request.get('is_new', None),
      'entry': entry,
      'tagnames': json.dumps(Tag.get_tagnames(), ensure_ascii=False),
      'status': self.request.get('status', None)
    }))

  def post(self, entry_id):
    entry = Entry.update_entry(entry_id, self.request2params(self.request))
    if entry is None:
      entry = Entry.get_entry(entry_id)
      self.redirect('/admin/entry/%d?status=fail' % entry.key.id())
    else:
      time.sleep(0.1)
      self.redirect('/admin/entry/%d?status=done' % entry.key.id())


class CreateEntryHandler(BaseHandler):
  def get(self):
    entry = {
      'date': datetime.datetime.now(),
      'is_published': True
    }
    template = jinja_environment.get_template('entry_edit.html')
    self.response.out.write(template.render({
      'is_new': True,
      'entry': entry,
      'tagnames': json.dumps(Tag.get_tagnames(), ensure_ascii=False),
      'status': self.request.get('status', None)
    }))

  def post(self):
    entry = Entry.update_entry(None, self.request2params(self.request), True)
    if entry is None:
      self.redirect('/admin/entry/new?status=fail')
    else:
      time.sleep(0.1)
      self.redirect('/admin/entry/%d?status=done&is_new=true' % entry.key.id())

class DeleteEntryHandler(BaseHandler):
  def get(self, entry_id):
    referer_path = self.request.referer.split('?')[0]
    if not Entry.delete_entry(entry_id):
      self.redirect('%s?status=del_fail' % referer_path)
    time.sleep(0.1)
    self.redirect('%s?status=del_done' % referer_path)

app = webapp2.WSGIApplication([
  (r'/admin/?', MainHandler),
  (r'/admin/entry/?', EntryListHandler),
  (r'/admin/entry/(\d+)/?', EditEntryHandler),
  (r'/admin/entry/(\d+)/del/?', DeleteEntryHandler),
  (r'/admin/entry/new/?', CreateEntryHandler)
], debug=True)
