#!/usr/bin/env python
# coding: utf-8
# Author: Somin Kobayashi

import webapp2
import os
import jinja2
import filters

jinja_environment = jinja2.Environment(
	loader = jinja2.FileSystemLoader(os.path.dirname(__file__))
)
jinja_environment.filters.update({
	'mark2html': filters.mark2html,
	'nl2br': filters.nl2br
})

class MainHandler(webapp2.RequestHandler):
	def get(self):
		template = jinja_environment.get_template('index.html')
		self.response.out.write(template.render())

class TestHandler(webapp2.RequestHandler):
	def get(self):
		markdown_sample = '''
h1 header
============

Paragraphs are separated by a blank line.

2nd paragraph. *Italic*, **bold**, `monospace`.

  * this one
  * that one
  * the other one
'''
		template = jinja_environment.get_template('test.html')
		self.response.out.write(template.render({
			'markdown_sample': markdown_sample
		}))

app = webapp2.WSGIApplication([
	('/', MainHandler),
	('/test', TestHandler)
], debug=True)
