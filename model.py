#!/usr/bin/env python
# coding: utf-8
# Author: Somin Kobayashi

from google.appengine.ext import db
import datetime

class BaseModel(db.Model):
    created_at = db.DateTimeProperty(auto_now_add=True)
    updated_at = db.DateTimeProperty(auto_now=True)

class Entry(BaseModel):
	title = db.StringProperty()
	body = db.TextProperty()
	date = db.DateTimeProperty()
	is_published = db.BooleanProperty(default=False)
	is_deleted = db.BooleanProperty(default=False)
