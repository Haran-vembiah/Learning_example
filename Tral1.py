# list1 = [1,2,3,4,5,6,7,8,9]
# print(list1.pop(2))
# print(f'After pop {list1}')
# print(list1.remove(5))
# print(f'After pop {list1}')
#
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


name_list = ('a','b','dsd','12')
def seperate_names(name_list):
    print(f"First name is {name_list[0]}")
    # print("dsda")
    listr_1 = ["Name","Address","Age","Sex"]
    for row,data in enumerate(listr_1):
        print(f"The row number {row} contains the data {data}")
seperate_names(name_list)




