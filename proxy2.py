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
            if tag == "div":
                for (variable, value)  in attrs:
                    if variable == 'class' and value == 'proxylistitem':
                        self.status = 1
        elif self.status == 1 and tag == 'div':
            self.status = 2
        elif self.status == 2 and tag == 'span':
            self.status = 3
        elif self.status == 4 and tag == 'span':
            self.status = 5
        elif self.status == 6 and tag == 'span':
            self.status = 7

    def handle_endtag(self, tag):
        if tag == "div":
            self.status = 0

    def handle_data(self, data):
        if self.status == 3:
            self.status = 4
            self.ip = data.strip()
        elif self.status == 5:
            self.status = 6
            self.port = data.strip()
        elif self.status == 7:
            self.status = 8
            if data.strip() == '高匿':
                if re.match(r'\d+\.\d+\.\d+\.\d+', self.ip) and re.match(r'\d+', self.port):
                    self.proxy_list.insert(random.randrange(len(self.proxy_list) + 1), (self.ip, self.port))


def run():
    ll = []
    h = httplib2.Http(timeout=30)

    try:
        response, content = h.request('http://www.proxy360.cn/Region/China', 'GET')
    except Exception, e:
        logging.error(e)
        return ll

    if response.status == 200:
        #content = content.decode('utf-8').encode('ascii', 'ignore')
        hp = MyHTMLParser(ll)
        hp.feed(content)
        #print content
        hp.close()

    return ll

if __name__ == "__main__":
    print run()
