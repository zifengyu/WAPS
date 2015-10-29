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
            if tag == "tr":
                self.status = 1
        elif self.status == 1 and tag == 'a':
            self.status = 2
        elif self.status == 3 and tag == 'td':
            self.status = 4

    def handle_endtag(self, tag):
        if tag == "tr":
            self.status = 0

    def handle_data(self, data):
        if self.status == 2:
            self.status = 3
            self.ip = data
        elif self.status == 4:
            self.status = 5
            self.port = data.strip()
            if re.match(r'\d+\.\d+\.\d+\.\d+', self.ip) and re.match(r'\d+', self.port):
                self.proxy_list.insert(random.randrange(len(self.proxy_list) + 1), (self.ip, self.port))


def run():
    ll = []
    h = httplib2.Http()

    for i in range(0, 200, 100):
        try:
            response, content = h.request('http://proxydb.net/list?protocol=http'
                                          '&anonlvl=4&only_keep_alive=1&minavail=80'
                                          '&maxtime=0&limit=100&ip_filter=&port_filter='
                                          '&host_filter=&country_filter=China&isp_filter='
                                          '&via_filter='
                                          '&offset=' + str(i), 'GET')
        except Exception, e:
            logging.error(e)
            return ll
        l = []
        if response.status == 200:
            content = content.decode('utf-8').encode('ascii', 'ignore')
            hp = MyHTMLParser(l)
            hp.feed(content)
            hp.close()
        if len(l) > 0:
            ll.extend(l)
        else:
            break

    return ll

if __name__ == "__main__":
    print run()
