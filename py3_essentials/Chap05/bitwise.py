#!/usr/bin/env python3
# Copyright 2009-2017 BHG http://bw.org/


n = 13
print(f'{n:b}')
# print(arr)
bin_list = [i for i in list(f'{n:b}')]
print(bin_list)
count =0
result = 0
for x in range(0,len(bin_list)):
    if bin_list[x] == '0':
        count = 0
    else:
        count+=1
        result = max(count,result)
print(result)