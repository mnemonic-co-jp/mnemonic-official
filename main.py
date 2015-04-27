# coding: utf-8
# Author: Somin Kobayashi

import webapp2
import os
import jinja2
import filters
import logging
import datetime
import settings

from user_agents import parse

from google.appengine.api import mail

from models import Entry
from utilities import is_pc

jinja_environment = jinja2.Environment(
  loader = jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates'))
)
jinja_environment.globals.update({
  'is_pc': is_pc()
})
jinja_environment.filters.update({
  'datetime2jdate': filters.datetime2jdate,
  'datetimeBySpec': filters.datetimeBySpec,
  'mark2html': filters.mark2html,
  'nl2br': filters.nl2br
})

class BaseHandler(webapp2.RequestHandler):
  pass

class MainHandler(BaseHandler):
  def get(self):
    template = jinja_environment.get_template('index.html')
    return self.response.out.write(template.render({
      'recent_entries': Entry.get_entries(num=5)
    }))

class PageHandler(BaseHandler):
  def get(self, name):
    try:
      template = jinja_environment.get_template(name + '.html')
    except IOError:
      template = jinja_environment.get_template('404.html')
    return self.response.out.write(template.render({}))

class BlogIndexHandler(BaseHandler):
  def get(self):
    template = jinja_environment.get_template('blog_list.html')
    return self.response.out.write(template.render({
      'entries': Entry.get_entries()
    }))

class BlogEntryHandler(BaseHandler):
  def get(self, entry_id):
    entry = Entry.get_entry(entry_id)
    if entry is None:
      template = jinja_environment.get_template('404.html')
      return self.response.out.write(template.render({}))
    entries = Entry.get_entry_titles()
    index = [e.key for e in entries].index(entry.key)
    previous_entry = entries[index - 1] if index > 0 else None
    next_entry = entries[index + 1] if index < len(entries) - 1 else None
    Entry.increment_views(entry_id)
    template = jinja_environment.get_template('blog_entry.html')
    return self.response.out.write(template.render({
      'is_pc': is_pc(),
      'entry': entry,
      'previous': previous_entry,
      'next': next_entry,
      'request_url': self.request.url
    }))

class FormPostHandler(BaseHandler):
  def get(self):
    template = jinja_environment.get_template('404.html')
    return self.response.out.write(template.render({}))

  def post(self):
    subject_template = jinja_environment.get_template('email/inquiry_subject.txt')
    subject = subject_template.render({
      'name': self.request.get('name')
    })
    body_template = jinja_environment.get_template('email/inquiry_body.txt')
    body = body_template.render({
      'name': self.request.get('name'),
      'phone': self.request.get('phone'),
      'email': self.request.get('email'),
      'message': self.request.get('message')
    })
    mail.send_mail(
      sender=settings.SENDER_ADDRESS,
      to=settings.RECIPIENT_ADDRESS,
      subject=subject,
      body=body
    )
    return self.redirect('/page/sent')

def Error404Handler(request, response, exception):
  logging.exception(exception)
  template = jinja_environment.get_template('404.html')
  return response.out.write(template.render({}))

def Error500Handler(request, response, exception):
  logging.exception(exception)
  template = jinja_environment.get_template('500.html')
  return response.out.write(template.render({}))

app = webapp2.WSGIApplication([
  (r'/', MainHandler),
  (r'/page/(\w+)/?', PageHandler),
  (r'/blog/?', BlogIndexHandler),
  (r'/blog/(\d+)/?', BlogEntryHandler),
  (r'/post', FormPostHandler)
], debug=True)

app.error_handlers[404] = Error404Handler
host = os.environ.get('HTTP_HOST', '')
if host != 'localhost:8084':
  app.error_handlers[500] = Error500Handler
