# coding: utf-8
# Author: Somin Kobayashi

import datetime
import markdown2

from utilities import utc2jst

def datetime2jdate(dt):
  if dt is None:
    return ''
  dt = utc2jst(dt)
  return u'%s年%s月%s日' % (dt.year, dt.month, dt.day)

def datetime2string(dt):
  if dt is None:
    return ''
  dt = utc2jst(dt)
  return dt.strftime('%Y/%m/%d %H:%M:%S')

def datetimeBySpec(dt, spec):
  if dt is None:
    return ''
  dt = utc2jst(dt)
  return dt.strftime(spec)

def mark2html(value):
  return markdown2.markdown(value, extras=['fenced-code-blocks'])

def nl2br(value):
  return value.replace('\n', '<br />\n')
