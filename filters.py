# coding: utf-8
# Author: Somin Kobayashi

import datetime
import markdown2

def datetime2JDate(dt):
  dt = _toJst(dt)
  return u'%s年%s月%s日' % (dt.year, dt.month, dt.day)

def _toJst(dt):
  return dt.replace(tzinfo=UtcTzinfo()).astimezone(JstTzinfo())

def mark2html(value):
  return markdown2.markdown(value)

def nl2br(value):
  return value.replace('\n', '<br />\n')

class UtcTzinfo(datetime.tzinfo):
  def utcoffset(self, dt): return datetime.timedelta(0)
  def dst(self, dt): return datetime.timedelta(0)
  def tzname(self, dt): return 'UTC'
  def olsen_name(self): return 'UTC'

class JstTzinfo(datetime.tzinfo):
  def utcoffset(self, dt): return datetime.timedelta(hours=9)
  def dst(self, dt): return datetime.timedelta(0)
  def tzname(self, dt): return "JST"
  def olsen_name(self): return 'Tokyo/Asia'
