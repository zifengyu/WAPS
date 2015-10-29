import csv

imsi = []
imei = []
with open('imsi.csv') as f:
    f_csv = csv.reader(f)
    for row in f_csv:
        imsi.append(row)

with open('imei.csv') as f:
    f_csv = csv.reader(f)
    for row in f_csv:
        imei.append(row)

f = open('result.csv', 'w')

for i in range(len(imei)):
    f.write(imei[i][0]+',')
    f.write(imsi[i][0]+',')
    f.write(imei[i][1]+',')
    f.write(imei[i][2]+',')
    f.write(imei[i][3]+',')
    f.write(imei[i][4]+',')
    f.write(imei[i][5]+'\n')
f.close()