list1 = [1, 2, 3, 4, 5, 6, 7, 8, 9]
list2 = [2, 5, 8, 10]

same_list = []
missing_list = []
same_list = [x for x in list1 if x in list2]
missing_list = [x for x in list1 if x not in list2]

print(same_list)
print(missing_list)
