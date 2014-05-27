#!/usr/bin/env python
# coding: utf-8
# Author: Somin Kobayashi

import webapp2
import os
import jinja2

jinja_environment = jinja2.Environment(
	loader = jinja2.FileSystemLoader(os.path.dirname(__file__))
)

class MainHandler(webapp2.RequestHandler):
    def get(self):
		template = jinja_environment.get_template('index.html')
		self.response.out.write(template.render())

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
