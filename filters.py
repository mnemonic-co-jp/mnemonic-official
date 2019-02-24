# coding: utf-8
# Author: Somin Kobayashi

import datetime
import markdown2

from utilities import utc2jst

def datetime2jdate(dt, full=False):
    if dt is None:
        return ''
    dt = utc2jst(dt)
    return_string = u'{0}年{1}月{2}日'.format(dt.year, dt.month, dt.day)
    if full:
        return return_string + ' ' + dt.strftime('%H:%M')
    return return_string

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
