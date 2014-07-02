#!/usr/bin/env python
# coding: utf-8
# Author: Somin Kobayashi

import webapp2
import os
import jinja2
import filters

jinja_environment = jinja2.Environment(
	loader = jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates'))
)
jinja_environment.filters.update({
	'mark2html': filters.mark2html,
	'nl2br': filters.nl2br
})

class MainHandler(webapp2.RequestHandler):
	def get(self):
		template = jinja_environment.get_template('index.jinja2')
		self.response.out.write(template.render())

class AboutHandler(webapp2.RequestHandler):
	def get(self):
		template = jinja_environment.get_template('about.jinja2')
		self.response.out.write(template.render())

class TestHandler(webapp2.RequestHandler):
	def get(self):
		template = jinja_environment.get_template('test.jinja2')
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
		template = jinja_environment.get_template('twitter_test.jinja2')
		self.response.out.write(template.render({
			'id_list': [
				'480238014119956480',
				'480238687272202240',
				'480239039262363648',
				'480239438878892032'
			]
		}))

app = webapp2.WSGIApplication([
	('/', MainHandler),
	('/about', AboutHandler),
	('/test', TestHandler),
	('/test/twitter', TwitterTestHandler)
], debug=True)
