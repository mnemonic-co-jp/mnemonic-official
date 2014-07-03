#!/usr/bin/env python
# coding: utf-8
# Author: Somin Kobayashi

import webapp2
import os
import logging
import jinja2
import filters

jinja_environment = jinja2.Environment(
	loader = jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates'))
)
jinja_environment.filters.update({
	'mark2html': filters.mark2html,
	'nl2br': filters.nl2br
})

def Error404Handler(request, response, exception):
	logging.exception(exception)
	template = jinja_environment.get_template('404.html')
	response.out.write(template.render())

def Error500Handler(request, response, exception):
	logging.exception(exception)
	template = jinja_environment.get_template('500.html')
	response.out.write(template.render())

class MainHandler(webapp2.RequestHandler):
	def get(self):
		template = jinja_environment.get_template('index.html')
		self.response.out.write(template.render())

class PageHandler(webapp2.RequestHandler):
	def get(self, name):
		try:
			template = jinja_environment.get_template(name + '.html')
		except IOError:
			template = jinja_environment.get_template('404.html')
		self.response.out.write(template.render())

class TestHandler(webapp2.RequestHandler):
	def get(self):
		template = jinja_environment.get_template('test.html')
		self.response.out.write(template.render({
			'markdown_sample': '''
h1 header
============

Paragraphs are separated by a blank line.

2nd paragraph. *Italic*, **bold**, `monospace`.

  * this one
  * that one
  * the other one
'''
		}))

class TwitterTestHandler(webapp2.RequestHandler):
	def get(self):
		template = jinja_environment.get_template('twitter_test.html')
		self.response.out.write(template.render({
			'id_list': [
				'480238014119956480',
				'480238687272202240',
				'480239039262363648',
				'480239438878892032'
			]
		}))

app = webapp2.WSGIApplication([
	(r'/', MainHandler),
	(r'/page/(\w+)/?', PageHandler),
	(r'/test', TestHandler),
	(r'/test/twitter', TwitterTestHandler)
], debug=True)
app.error_handlers[404] = Error404Handler
app.error_handlers[500] = Error500Handler