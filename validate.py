import csv
import collections

if __name__ == '__main__':

    print 'validating phones'

    phones = []
    apps = []
    with open('phone.csv') as f:
        f_csv = csv.reader(f)
        for row in f_csv:
            phones.append(row)

    imsi_list = [phone[1] for phone in phones]
    imei_list = [phone[0] for phone in phones]
    print 'len(imsi) =', len(imsi_list)
    print 'unique imsi =', len(set(imsi_list))
    print [item for item, count in collections.Counter(imsi_list).items() if count > 1]

    print 'len(imei) =', len(imei_list)
    print 'unique imei =', len(set(imei_list))
    print [item for item, count in collections.Counter(imei_list).items() if count > 1]
