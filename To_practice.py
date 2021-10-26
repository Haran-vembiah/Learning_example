# my_dict = {"Name": "Haran", "age":21, "gender":"male"}
# print(my_dict.items())
# print(my_dict.keys())
# print(my_dict.values())
#
# for x in my_dict.items():
#     print(x)
#
# for x in my_dict.values():
#     print(x)


# pop and remove method of list
# list1 = [1, 2, 3, 4, 5, 6, 7, 8, 9]
# print(list1)
# popped_ele = list1.pop()
# print(popped_ele)
# print(list1)
# removed_ele = list1.remove(1)
# print(removed_ele)
# print(list1)
# popped_ele = list1.pop(3)
# print(popped_ele)
# print(list1)

#
# str1 = "Haran"
# print(str1[::-1])
# print(str1[0:5:2])
#
# list1 = []
# Dict = {'Tim': 18, 'Charlie': 12, 'Tiffany': 22, 'Robert': 25}
# print("Students Name: %s" % list(Dict.items()))
# for x, y in Dict.items():
#     list1.append(x)
#     list1.append(y)
# print(list1)
# print(list(Dict.keys()))


# list1 = [1, 2, 3, 4, 5, 6, 7, 8, 9]
# print(list1)
# del list1['1']
# print(list1)
# from collections import defaultdict
#
# list1 = ['a', 'b', 'c']
# list2 = [1, 2, 3]
# my_dict = defaultdict(list)
# for x in list1:
#     for y in list2:
#         my_dict[x].append(y)
# print(my_dict)
# my_dict['a'].append('20')
# print(my_dict)

#
# for x in range(5, 10):
#     print(x)

# def inc(a, b=1):
#     return (a + b)
#
#
# a = inc(1)
# a = inc(a, a)
# print(a)
def sam(number):
    if (number >= 1000):
        print(4)
    elif (number >= 100):
        print(3)
    elif (number >= 10):
        print(2)
    else:
        print(1)


sam(9999)
