# coding: utf-8
# Author: Somin Kobayashi

import webapp2
import os
import jinja2
import logging
import settings

from google.appengine.api import users

jinja_environment = jinja2.Environment(
  loader = jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates/admin'))
)

class BaseHandler(webapp2.RequestHandler):
  def is_admin(self):
    user = users.get_current_user()
    if user == None:
      self.redirect(users.create_login_url(self.request.uri))
    if user != None and user.nickname() == settings.ADMIN_USER:
      return True
    return False

class MainHandler(BaseHandler):
  def get(self):
    if not self.is_admin():
      return
    template = jinja_environment.get_template('index.html')
    self.response.out.write(template.render())

app = webapp2.WSGIApplication([
  (r'/admin/?', MainHandler)
], debug=True)
