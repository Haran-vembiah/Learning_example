# sorted and rounding list
list1 = [12, 13, 15, 16, 1, 2, 3]
print(len(list1))
mid = int(len(list1) / 2)
first_list = list1[:mid]
sec_list = list1[mid:]
print(first_list)
print(sec_list)
if first_list[0] > sec_list[0]:
