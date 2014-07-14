# coding: utf-8
# Author: Somin Kobayashi

import webapp2
import os
import jinja2
import filters
import json
import logging
import datetime

from models import Entry

jinja_environment = jinja2.Environment(
  loader = jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates'))
)
jinja_environment.filters.update({
  'datetime2JDate': filters.datetime2JDate,
  'mark2html': filters.mark2html,
  'nl2br': filters.nl2br
})

class BaseHandler(webapp2.RequestHandler):
  pass

class MainHandler(BaseHandler):
  def get(self):
    template = jinja_environment.get_template('index.html')
    self.response.out.write(template.render())

class PageHandler(BaseHandler):
  def get(self, name):
    try:
      template = jinja_environment.get_template(name + '.html')
    except IOError:
      template = jinja_environment.get_template('404.html')
    self.response.out.write(template.render())

class BlogIndexHandler(BaseHandler):
  def get(self):
    entries = Entry.get_entries().fetch()
    template = jinja_environment.get_template('entries.html')
    self.response.out.write(template.render({
      'entries': entries
    }))

class BlogEntryHandler(BaseHandler):
  def get(self, entry_id):
    entry = Entry.get_entry(entry_id)
    if entry is None:
      template = jinja_environment.get_template('404.html')
      self.response.out.write(template.render())
    else:
      template = jinja_environment.get_template('entry.html')
      self.response.out.write(template.render({
        'title': entry.title,
        'date': entry.date
      }))

class BlogTestHandler(BaseHandler):
  def get(self):
    Entry.create_entry()

def Error404Handler(request, response, exception):
  logging.exception(exception)
  template = jinja_environment.get_template('404.html')
  response.out.write(template.render())

def Error500Handler(request, response, exception):
  logging.exception(exception)
  template = jinja_environment.get_template('500.html')
  response.out.write(template.render())

app = webapp2.WSGIApplication([
  (r'/', MainHandler),
  (r'/page/(\w+)/?', PageHandler),
  (r'/blogs/?', BlogIndexHandler),
  (r'/blog/(\d+)/?', BlogEntryHandler),
  (r'/blog/test', BlogTestHandler),
  (r'/blog/test', BlogTestHandler)
], debug=True)
app.error_handlers[404] = Error404Handler
app.error_handlers[500] = Error500Handler