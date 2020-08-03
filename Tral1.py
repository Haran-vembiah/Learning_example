# list1 = [1,2,3,4,5,6,7,8,9]
# print(list1.pop(2))
# print(f'After pop {list1}')
# print(list1.remove(5))
# print(f'After pop {list1}')
#
import re
from random import random

# dict1 = {'name': 'haran','name1': 'haran1','name2': 'haran2','name3': 'haran3'}
# print(dict1.items())
# sam_nam = "name2"
# print(dict1.get(sam_nam))
# for ite in dict1.items():
#     print(ite)
#     print(type(ite))
# print(dict1.keys())
# for keys in dict1.keys():
#     print(keys)
#     print(type(keys))
# print(dict1.values())
# list1 = [1,1,1,2,5,"gtfdg","gfdgfd","gfdgfdg", "Bala"]
# print(list1.count("Bala"))
# print(list1[5])
# print(f'Tha actual list is {list1}')
# list2 = set(list1)
# print(list2)
# list1[0] = 10
# print(type(list2))
# print(f'Sorted list is {list2}')
# print(list(list2))
# print(type(list2))
#
#



#
# name = input().split( )
# fname = name[0]
# sname = name[1]
# tname = name[2]
# print(f'{fname} ')
# print(f'{sname} ')
# print(f' {tname}')




#
# def review(s):
#     for x in range(0, len(s), 2):
#         print(s[x],end='') #Here the end ='' prints in the same line instead of printing in a new line
#     print(" ",end='')
#     for y in range(1, len(s), 2):
#         print(s[y],end="")
#     print(" ")
#
#
# t = int(input())
# for i in range(0, t):
#     s = list(input())
#     review(s)



# list_1 = [x*3 for x in range(0,13) ]
# print(list_1)

# str_1 = input("give space seperated")
# str_2 = str_1.split(" ")
# print(str_2[0])
# print(str_2[1])
# print(str_2[2])

# str_4 = "welcome"
# od_str = " "
# even_str = " "
# j=0
# for i in str_4:
#     if j%2 == 0:
#         od_str +=i
#     else:
#         even_str +=i
#     j+=1
# print(od_str)
# print(even_str)

# list_new = [1,2,3,"bala","haran"]
# for x in list_new:
#     if x == "bala":
#         print(x)
#         break
#         print("also")
x=10
kwargs = {'a':x,'b':11,'c':13}

def sam_func(**kwargs):
    print(kwargs['a'])
    print(kwargs['b'])
    print(len(kwargs))
    if len(kwargs)> 2:
        print(kwargs['c'])
    print()
    print(kwargs.items())
    print(kwargs.keys())
    kwargs['a'] = 100

def sam_func1(**kwargs):
    print(kwargs['a'])


sam_func(**kwargs)
kwargs['a'] = 100
sam_func1(**kwargs)

a1 = [1,2,34]
b1 = []
if a1:
    print('a1 has data')
if not b1:
    print('b1 empty')

