import random
import csv

head = '86711102076'
device = 'MUTUCU K1,MUTUCU,720,1280,4.4.4'


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

index = 100 + random.randint(1, 19)

imsi = []
with open('imsi.csv') as f:
    f_csv = csv.reader(f)
    for row in f_csv:
        imsi.append(row)

f = open('phone.csv', 'a')
i = 0

while index < 1000:
    p = head + str(index)
    p += str(calculate_luhn(p))
    f.write('\n' + p + ',' + imsi[i][0] + ',' + device)
    index += random.randint(3, 29)
    i += 1

f.close()

f = open('imsi.csv', 'w')
for j in range(i, len(imsi)):
    f.write(imsi[j][0] + '\n')
f.close()
