#!/usr/bin/env python

from BeautifulSoup import BeautifulSoup
from syck import *
import re; ## require 'yaml'
import sys, os

HTMLHEADBODY = """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
"http://www.w3.org/TR/html4/loose.dtd">
<html> <head><meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">
<title>Untitled Document</title></head> <body>"""
REDDIT_FILE_DIR="C:\\kacc\\pyrb\\reddit_pages"
                
class RedditFilesParser(object):
    redd_urls={}
    for redd_file in os.listdir(REDDIT_FILE_DIR):
        soup = BeautifulSoup(redd_file)
        
        
