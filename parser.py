#!/usr/bin/env python
import sys
with open(sys.argv[1], 'r') as df:
    temp = df.read().splitlines()
data_line = 0
parsed = []
for item in temp:
    if 'Data' in item:
        data_line += 1
    else:
        if 1 <= data_line <= 9:
            result = item.split()
            if len(result) > 12:
                parsed.append(result[1:])
            data_line += 1
output_fn = sys.argv[1].split('.')[0] + '_result' + '.csv'
index = 1
with open(output_fn, 'w') as dw:
    for j in range(12):
        for i in range(8):
            dw.write(str(index) + ',' + parsed[i][j] + '\n')
            index += 1
    dw.close()
