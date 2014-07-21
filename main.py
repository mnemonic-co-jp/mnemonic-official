# coding: utf-8
# Author: Somin Kobayashi

import webapp2
import os
import jinja2
import filters
import json
import logging
import datetime
import settings

from google.appengine.api import mail
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
    template = jinja_environment.get_template('blog_list.html')
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
      Entry.increment_views(entry_id)
      template = jinja_environment.get_template('blog_entry.html')
      self.response.out.write(template.render({
        'entry': entry,
        'request_url': self.request.url
      }))

class BlogTestHandler(BaseHandler):
  def get(self):
    Entry.create_entry()

class FormPostHandler(BaseHandler):
  def get(self):
    template = jinja_environment.get_template('404.html')
    self.response.out.write(template.render())

  def post(self):
    mail.send_mail(
      sender=settings.SENDER_ADDRESS,
      to=settings.RECIPIENT_ADDRESS,
      subject='【Mnemonic】%sさんからのお問い合わせ' % self.request.get('name').encode('utf-8'),
      body="""
Mnemonicウェブサイトに以下の問い合わせがありました。

氏名：%s
電話番号：%s
メールアドレス：%s

内容：
%s

以上です。
""" % (
        self.request.get('name').encode('utf-8'),
        self.request.get('phone').encode('utf-8'),
        self.request.get('email').encode('utf-8'),
        self.request.get('message').encode('utf-8')
      )
    )
    self.redirect('/page/sent')

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
  (r'/blog/?', BlogIndexHandler),
  (r'/blog/(\d+)/?', BlogEntryHandler),
  (r'/blog/test', BlogTestHandler),
  (r'/post', FormPostHandler)
], debug=True)
app.error_handlers[404] = Error404Handler
app.error_handlers[500] = Error500Handler
