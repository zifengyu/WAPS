# coding=utf-8

import httplib2
from HTMLParser import HTMLParser
import re
import random
import logging


class MyHTMLParser(HTMLParser):
    def __init__(self, proxy_list):
        HTMLParser.__init__(self)
        self.status = 0
        self.ip = None
        self.port = None
        self.proxy_list = proxy_list

    def handle_starttag(self, tag, attrs):
        if self.status == 0:
            if tag == "ul":
                self.status = 1
        elif self.status == 1 and tag == 'li':
            for (variable, value) in attrs:
                if variable == 'class' and value == 'proxy':
                    self.status = 2

    def handle_endtag(self, tag):
        if tag == "ul":
            self.status = 0

    def handle_data(self, data):
        if self.status == 2:
            self.status = 3
            if data.find(':') > 0:
                self.ip, self.port = data.strip().split(':')
                if re.match(r'\d+\.\d+\.\d+\.\d+', self.ip) and re.match(r'\d+', self.port):
                    self.proxy_list.insert(random.randrange(len(self.proxy_list) + 1), (self.ip, self.port))


def run():
    ll = []
    #h = httplib2.Http(timeout=30)

    #try:
    #    response, content = h.request('https://proxy-list.org/english/search.php?'
    #                                  'search=CN.elite&country=CN&type=elite&port=any&ssl=any', 'GET')
    #except Exception, e:
    #    logging.error(e)
    #    return ll

    #if response.status == 200:
    #    content = content.decode('utf-8').encode('ascii', 'ignore')
    #    hp = MyHTMLParser(ll)
    #    hp.feed(content)
        #print content
    #    hp.close()

    return ll

if __name__ == "__main__":
    print run()
