#!/usr/bin/env python
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
		entries = Entry.get_entries()
		for entry in entries:
			logging.debug(entry.title)
			logging.debug(entry.twitter_ids[0])
		self.response.out.write(u'ブログのインデックスページ')

class BlogHandler(webapp2.RequestHandler):
	def get(self, id):
		entry = Entry(
			title='hoge'+id,
			twitter_ids=[111111, 22222],
			body=u'あああああ\nいいいいい',
			tags=['hoge', 'fuga']
		)
		entry.put()
		self.response.out.write(u'ブログの個別ページ: ' + id)

class TestHandler(BaseHandler):
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

class TwitterTestHandler(BaseHandler):
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
	(r'/blog/(\d+)/?', BlogHandler),
	(r'/test', TestHandler),
	(r'/test/twitter', TwitterTestHandler)
], debug=True)
app.error_handlers[404] = Error404Handler
app.error_handlers[500] = Error500Handler