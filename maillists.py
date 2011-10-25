#!/usr/bin/env python
## from BeautifulSoup import BeautifulSoup
from ElementTree import ElementTree
import sys, urllib2
import time

class RubyListParser(object):
    def __init__(url):
        self.url=url
        urlreq=urllib2.Request(url)
        handle=urllib2.urlopen(urlreq)
        self.url_html=handle.read()
    def parse():
        tree = ElementTree.fromstring(self.url)
        
class TestOneURL(object):
    def __init__(*initargs):
        sys.stdout.write( *initargs)
        url=r'http://blade.nagaokaut.ac.jp/cgi-bin/scat.rb/ruby/ruby-talk/175825'
        rp=RubyListParser(url)
    
if __name__=='__main__':
    print time.ctime(time.time() )
    rp=RubyListParser(r'http://blade.nagaokaut.ac.jp/cgi-bin/scat.rb/ruby/ruby-talk/175825')
 #   cl=TestOneURL()
