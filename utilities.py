# coding: utf-8
# Author: Somin Kobayashi

import os
import datetime

from user_agents import parse

def is_pc():
    ua_string = os.environ.get('HTTP_USER_AGENT', '')
    user_agent = parse(ua_string)
    return user_agent.is_pc

def utc2jst(dt):
    return dt.replace(tzinfo=UtcTzinfo()).astimezone(JstTzinfo())

def jst2utc(dt):
    return dt.replace(tzinfo=JstTzinfo()).astimezone(UtcTzinfo())

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
