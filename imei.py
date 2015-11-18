import random
import csv


head = '35586705315'
device = 'HTC 802t,htccn_chs,1080,1920,4.1'


def luhn_checksum(card_number):
    def digits_of(n):
        return [int(d) for d in str(n)]
    digits = digits_of(card_number)
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    checksum = sum(odd_digits)
    for d in even_digits:
        checksum += sum(digits_of(d*2))
    return checksum % 10


def calculate_luhn(partial_card_number):
    check_digit = luhn_checksum(int(partial_card_number) * 10)
    return check_digit if check_digit == 0 else 10 - check_digit

index = 100 + random.randint(1, 20)

imsi = []
with open('imsi.csv') as f:
    f_csv = csv.reader(f)
    for row in f_csv:
        imsi.append(row)

f = open('imei.csv', 'w')
i = 0

while index < 1000:
    p = head + str(index)
    p += str(calculate_luhn(p))
    f.write(p + ',' + imsi[i][0] + ',' + device + '\n')
    index += random.randint(3, 19) + 1
    i += 1

f.close()
