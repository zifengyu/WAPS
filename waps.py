import hashlib
import httplib2
import time
import random
from HTMLParser import HTMLParser
import csv
import logging

import proxy

class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            if len(attrs) == 0:
                pass
            else:
                for (variable, value) in attrs:
                    if variable == "href":
                        self.links.append(value)


def get_client():
    phones = []
    apps = []
    with open('phone.csv') as f:
        f_csv = csv.reader(f)
        for row in f_csv:
            phones.append(row)

    with open('app.csv') as f:
        f_csv = csv.reader(f)
        for row in f_csv:
            apps.append(row)

    a_phone = phones[random.randint(0, len(phones)-1)]
    a_app = apps[random.randint(0, len(apps)-1)]

    logging.info('[Client] app={0} phone={1}'.format(str(a_app), str(a_phone)))

    udid = a_phone[0]
    imsi = a_phone[1]
    device_name = a_phone[2]
    device_brand = a_phone[3]
    device_width = a_phone[4]
    device_height = a_phone[5]
    os_version = a_phone[6]
    app_id = a_app[0]
    app_version = a_app[1]
    act = a_app[2]
    sdk_version = a_app[3]

    m = hashlib.md5()
    s = 'kingxiaoguang@gmail.com' + udid + app_id
    m.update(s)
    y = m.hexdigest()

    client = 'app_id=' + app_id + \
           '&udid=' + udid + \
           '&imsi=' + imsi + \
           '&net=mobile' \
           '&base=wapx.cn' \
           '&app_version=' + app_version + \
           '&sdk_version=' + sdk_version + \
           '&device_name=' + device_name + \
           '&device_brand=' + device_brand + \
           '&y=' + y + \
           '&device_type=android' + \
           '&os_version=' + os_version + \
           '&country_code=CN' \
           '&language=zh' \
           '&act=' + act + \
           '&channel=WAPS' \
           '&device_width=' + device_width + \
           '&device_height=' + device_height

    client = client.replace(' ', '%20')

    return client


def get_proxy_list():
    return proxy.run()


def run():
    proxy_list = get_proxy_list()
    logging.info('[ProxyList] total={0}'.format(len(proxy_list)))

    sleep_time = [7200, 7200, 7200, 7200, 7200, 3600, 360, 253, 113, 53, 21, 7, 3, 3, 5, 5, 7, 5, 7, 3, 1, 7, 11, 13, 133, 3600]

    for proxy_ip, proxy_port in proxy_list:
        logging.info('[Proxy] ip={0} port={1}'.format(proxy_ip, proxy_port))
        proxy_info = httplib2.ProxyInfo(httplib2.socks.PROXY_TYPE_HTTP_NO_TUNNEL, proxy_ip, int(proxy_port))
        h = httplib2.Http(timeout=15, proxy_info=proxy_info)

        client = get_client()
        logging.info('[Client URL] {0}'.format(client))

        try:
            response, content = h.request('http://app.wapx.cn/action/connect/active?' + client + '&at=' + str(int(time.time() * 1000)), 'GET')
            logging.info('[Active] status={0}'.format(response.status))

            if response.status == 200:
                for i in range(8):
                    response, content = h.request('http://app.wapx.cn/action/ad/show?' + client, 'GET')
                    logging.info('[Show] status={0}'.format(response.status))
                    if response.status == 200:
                        if random.randint(1, 20) == 2:
                            hp = MyHTMLParser()
                            hp.feed(content)
                            hp.close()
                            is_clicked = False
                            for link in hp.links:
                                if 'cpc' in link:
                                    cpc_link = ('http://app.wapx.cn' + link).replace(' ', '%20')
                                    logging.info('[CPC] url={0}'.format(cpc_link))
                                    time.sleep(random.randint(1, 13))
                                    response, content = h.request(cpc_link, 'GET', redirections=10)
                                    logging.info('[CPC] status={0}'.format(response.status))
                                    is_clicked = True
                            if is_clicked:
                                logging.info('[Sleep] random time={0}'.format(sleep_time[time.localtime().tm_hour]))
                                time.sleep(random.randint(1, sleep_time[time.localtime().tm_hour]))
                                break
                    else:
                        break
                    logging.info('[Sleep] time=20')
                    time.sleep(20)
                else:
                    logging.info('[Sleep] random time={0}'.format(sleep_time[time.localtime().tm_hour]))
                    time.sleep(random.randint(1, sleep_time[time.localtime().tm_hour]))
        except Exception, e:
            logging.error(e)

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', filename='waps.log', level=logging.INFO)
    run()

