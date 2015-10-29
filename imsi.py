import httplib2
from HTMLParser import HTMLParser
import time


class MyHTMLParser(HTMLParser):
    def __init__(self, imsi_list):
        HTMLParser.__init__(self)
        self.status = 0
        self.output = open('imsi.csv', 'a')
        self.imsi_list = imsi_list

    def handle_starttag(self, tag, attrs):
        pass

    def handle_endtag(self, tag):
        pass

    def handle_data(self, data):
        data = data.strip()
        if len(data) == 15 and data.startswith('460'):
            if data not in self.imsi_list:
                self.imsi_list.append(data)
                self.output.write(data)
                self.output.write('\n')
                self.output.flush()


def run():
    ml = []
    proxy_info = httplib2.ProxyInfo(httplib2.socks.PROXY_TYPE_HTTP_NO_TUNNEL, '117.177.243.42', 82)
    h = httplib2.Http(proxy_info=proxy_info)
    index = -1

    url = 'http://www.soimsi.com/imsi.html'



    while index < len(ml):
        response, content = h.request(url, 'GET')

        if response.status == 200:
            content = content.decode('utf-8').encode('ascii', 'ignore')
            hp = MyHTMLParser(ml)
            hp.feed(content)
            hp.close()

        index += 1
        if index < len(ml):
            url = 'http://www.soimsi.com/phone_' + ml[index] + '.html'

        time.sleep(5)


if __name__ == "__main__":
    print run()
