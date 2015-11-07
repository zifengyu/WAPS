# coding=utf-8

import httplib2
from HTMLParser import HTMLParser
import re
import random
import logging
import time


class MyHTMLParser(HTMLParser):
    def __init__(self, proxy_list):
        HTMLParser.__init__(self)
        self.status = 0
        self.ip = None
        self.port = None
        self.proxy_list = proxy_list

    def handle_starttag(self, tag, attrs):
        if self.status == 0:
            if tag == "tr":
                self.status = 1
        elif self.status == 1 and tag == 'td':
            self.status = 2
        elif self.status == 3 and tag == 'td':
            self.status = 4

    def handle_endtag(self, tag):
        if tag == "tr":
            self.status = 0

    def handle_data(self, data):
        if self.status == 2:
            self.status = 3
            self.ip = data.strip()
        elif self.status == 4:
            self.status = 5
            self.port = data.strip()
        elif self.status == 5 and data.strip() == '高匿':
            self.status = 6
            if re.match(r'\d+\.\d+\.\d+\.\d+', self.ip) and re.match(r'\d+', self.port):
                #exist_ips = ['.'.join(ip.split('.')[:2]) for ip, port in self.proxy_list]
                #if '.'.join(self.ip.split('.')[:2]) not in exist_ips:
                self.proxy_list.insert(random.randrange(len(self.proxy_list) + 1), (self.ip, self.port))
                #self.proxy_list.append((self.ip, self.port))


def run():
    ll = []

    h = httplib2.Http(timeout=30)

    for i in range(1, 20):

        try:

            time.sleep(random.randint(3, 5))
            response, content = h.request('http://www.haodailiip.com/guonei/' + str(i), 'GET')

        except Exception, e:
            logging.error(e)
            l2 = []
            l3 = []

            for ip, port in ll:
                if '.'.join(ip.split('.')[:3]) not in l3:
                    l2.append((ip, port))
                    l3.append('.'.join(ip.split('.')[:3]))
            return l2

        l = []

        if response.status == 200:
            #print content
            #content = content.decode('utf-8').encode('ascii', 'ignore')
            hp = MyHTMLParser(l)
            hp.feed(content)
            hp.close()

        if len(l) > 0:
            ll.extend(l)
        else:
            pass

    l2 = []
    l3 = []

    for ip, port in ll:
        if '.'.join(ip.split('.')[:3]) not in l3:
            l2.append((ip, port))
            l3.append('.'.join(ip.split('.')[:3]))

    return l2

if __name__ == "__main__":
    print run()
