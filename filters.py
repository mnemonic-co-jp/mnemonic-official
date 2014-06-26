#!/usr/bin/env python
# coding: utf-8
# Author: Somin Kobayashi

import markdown2

def mark2html(arg):
	return markdown2.markdown(arg)

def nl2br(arg):
    return arg.replace('\n', '<br />\n')