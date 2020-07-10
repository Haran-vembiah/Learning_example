# =================================================================== Python Basics =======================================================================
# Printout the second element of each tuple using for loop
# elements = ((1,2), (3,4), (5,6))
# for i,j in elements:
#     print(i)
#     print(j)

# Print sum of three variables
# a =1
# b=2
# c=3
# print(a+b+c)
# ========
# print(sum((a,b,c)))   #It sums the value of all the three variables
# ==========

# Tuple to dictionary
# customer = (
#     ('id','98698761'),
#     ('name', 'marry'),
#     ('surname', 'smith'),
#     ('rented_books', 3 )
#     )
# my_dict = {}
# for key,value in customer:
#     my_dict[key] = value
# print(my_dict)
# ==========
# print(dict(customer))      #It converts the tuple into dict
# ==========


# loop over the list passwords and in each iteration, Printout the items, if the items containing the strings 'ab' and 'ba' inside the list
# passwords = ['ccavfb', 'baaded', 'bbaa', 'aaeed', 'vbb', 'aadeba', 'aba', 'dee', 'dade', 'abc', 'aae', 'dded', 'abb', 'aaf', 'ffaec']
# for pwds in passwords:
#     if 'ab' in pwds or 'ba' in pwds:
#         print(pwds)


# Implement a function that:
# (1 ) takes a list and another object as parameters
# (2) checks if that object is in the list
# (3) adds the object to the list if the object is not in the list
# (4) returns the list.
# def sample(list_sam, sam_obj):
# #     list1 = list_sam
# #     if sam_obj not in list1:
# #         list1.append(sam_obj)
# #     return list1
# # list_sam = ["anand", "bala", "Haran"]
# # new_list = sample(list_sam,"Surya")
# # print(new_list)

# Integers of non Empty Lists
# Loop through the elements list and print out the first item of each list if the item is an integer.
# elements = [
#     [1, 4, 6, 7],
#     [4, 5, 6],
#     [6, 7, 8],
#     [],
#     ["nodata", "nodata"],
#     [1, 3]
#             ]
#
# for inner_list in elements:
#     for inner_elements in inner_list:
#         if type(inner_elements) is int:
#             print(inner_elements)
#         break

# =======================
# for inner_list in elements:
#     if inner_list and isinstance(inner_list[0],int):             #Using isinstance() it returns boolean if the given object is of given type or not
#         print(inner_list[0])
# =======================

# *************************************************************Python basics ends here********************************************************************************************************************





# ================================================================Functions=============================================================================================================
# Simple Sum
# Implement a function that takes two numbers as parameters and returns their sum.
# def sum_num(a,b):
#     return(sum((a,b)))
# print(sum_num(1,7))


# Sequence Index
# Implement a function that takes a list as parameter and returns the first item of the list.
# def sam_funct(list1):
#     return list1[0]
# print(sam_funct([12,3,4,5]))



# Sequence Last Item
# Implement a function that takes a list as parameter and returns the last item of the list.
# def last_elem(list1):
#     return list1[-1]
# print(last_elem([12,3,4,15]))

# Sequence First and Last
# Implement a function that takes a list as parameter and returns the first and the last item of the list.
# def last_elem(list1):
#     return list1[0], list1[-1]
# print(last_elem([12,3,4,15]))


# List Maximum
# Complete the foo function so that it returns the maximum number of mylist .
# def max_elem(list1):
#     return max(list1)
# print(max_elem([12222,3,4,150]))


# List Concatenation
# Implement a function that takes three lists as parameters and returns one concatenated list.
# def list_concat(list1,list2,list3):
#     return list1+list2+list3
#
# print(list(set(list_concat([1,2,3],[6,5,8],[2,5,8]))))

# Multiple Arguments Call
# Insert the proper value/-s inside foo() in line 5 so that the script outputs (2, 6, 10)
# Do not change the foo function definition. Just write the proper values in the function call.
# def foo(*args):
#     double_list = [x * 2 for x in args]
#     return double_list
#
# print(foo(1,3,5))



# Multiple Arguments Function Definition
# Implement a function that takes an indefinite number of arguments and returns a list containing all the argument values.
# def args_list(*list_values):
#     return list(list_values)
#
# print(args_list(1,2,"Name",3,"age"))


# Multiple Keyword Arguments
# Implement a function that takes an indefinite number of keyword arguments and returns a dictionary contain•ng all the argument
# names and the argument values.
# def kwargs_dict(**kwargs):
#     return kwargs
#
# print(kwargs_dict(a=1,b=2,c=3))


# Concatenate Lists Indefinite
# Implement a function that takes an indefinite number of lists and returns the concatenated list
# def args_list(*list_values):
#     new_list = []
#     for list_item in list_values:
#         new_list = new_list + list_item
#     return list(new_list)
#
# print(args_list([1,2],[3,4,5],[6,7,8]))


# True if All
# Implement a function that
# (1 ) takes an indefinite number of lists as arguments
# (2) returns True if all ists have at least one item
# (3) returns False if one or more lists are empty.
# For example, if I called the function you have to define it would behave like below:
# def funct_all(*args):
#     return all(args)
#
# print(funct_all([1,23],[2,5],[],[5,9]))


# Function of Function
# Define another function below the foo function. That other function should return the foo function.
# Note that I said the foo fun on, not the foo function call.
# def foo():
#     return "Hello"
# def fhoo():
#     return foo
#
# print(type(fhoo()))


# Commented Functions
# Suppose your colleague started to write two functions but then he/she got busy with another task and left the task to you. Try to complete
# those two function definitions based on the comments your colleague left and the named he/she used to name the functions.
# Function gets a list, converts it to tuple and returns the tuple
# def list_to_tuple(lst):
#     return tuple(lst)

# Function gets any Python class object (e.g. str, int, float, etc) and returns the object name as string (i.e. 'str', 'int', 'float')
# def object_to_string(object):
#     return object.__name__

# print(f"The converted tuple is {list_to_tuple([1,2,3,4])}")
# print(f"The type of given object is {object_to_string(float)}")


# *************************************************************Functions ends here********************************************************************************************************************





# ================================================================Data structures and algorithm =============================================================================================================


# Decimal Universe
# Print out all numbers from 0 to 10 with an increment of 0.1 .
# Expected output:
# 0.1
# 0.2
# 0.3
# ...
# ...
# ...
# 9.9
# 10.0
# for i in(x/10 for x in range(0,101)):
#     print(i)

# Number Info
# Implement a function that:
# (1) takes a number as parameter
# (2) returns a dictionary that has information about the sign( 'negative' ,'positive' or 'Zero') and the parity ('odd', 'even', 'non-integer')
#
# For example, if I called your function as below it would return:
# foo(10) ('sign': 'positive', 'parity': 'even')
# foo(-2) ('sign': 'negative', 'parity': 'even )
# foo(-3) ('sign': 'negative', 'parity': 'odd')
# def number_info(numb):
#     return dict(sign ="positive" if numb > 0 else "negative" if numb < 0 else "zero",
#                 parity = "even" if numb%2==0 else "odd" if numb%2==1 else "non integer")
#
# print(number_info(01))



# Sequence Last Item If Last Item
# Implement a function that:
# (1 ) takes a list as parameter
# (2) returns the last item of the list
# (3) returns the string "Empty List" if the input list has no items.
# def last_item(list):
#     return list[-1] if list else "Empty List"
#
# print(last_item([]))


# The Inside of a List
# Implement a function that takes a list as parameter and returns a list with all but the first and the last item of the input list.
# For instance, if i was to call your function with foo(2, 19, 99, l09)) the output should be 19 and  99,
# def inside_list(list):
#     return list[1:-1:]
# print(inside_list([1,2,3,4,5,6,7,8,9]))

# Remove if Too Big and Add New
# Implement a function that:
# (1 ) takes a list and an object as arguments
# (2) if the list has three items remove the first item of the list and append the object to the end of the list
# (3) return the modified list or return None if the list didn't have three items.
# def remove_from_list(list, object):
#
#     if len(list) == 3:
#         list.pop(0)
#         list.append(object)
#         return list
#     else:
#         return None

# print(remove_from_list([1,2,3],"value"))




# Every Seven
# Implement a function that takes a list as parameter and returns the first item and then every subsequent 7th item of the input list.
# the output contains the Ist element, 8th, 15th, 22nd, and so every item at a step of7.
# def every_seventh(list):
#     return list[0:len(list):7]
#
# print(every_seventh([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25]))


# Five Every Seven
# In the previous exercise you created a function that returned the Ist item of the input list, the 8th item, the 1 5th, and so on every item ata
# step of7. In this exercise you should create a similar function but instead of returning 1 item at a step of 7, you should return 5 items at a
# step of 7.
# So, the function should return the Ist item, 2nd, 3rd, 4th, 5th, 8th, 9th, 10th, 1 lth,12th, 15th, 16th, 17th, 18th, 19th, 22nd, 23rd, and so on.
# def five_every_seventh(list):
#     seventh_list = list[0:len(list):7]
#     new_list = [1,2]
#     print(new_list)
#     print(type(new_list))
#     # return seventh_list
#     for elem_ in seventh_list:
#         print(elem_)
#         print(type(new_list))
#         new_list = new_list.append(list[elem_-1:elem_+4:])
#         return new_list
#
# print(five_every_seventh([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]))


# Middle value from the list of odd values
def odd_list(mylist):
    mid_index = int(len(mylist) / 2)
    print(mylist[mid_index])

odd_list([1, 2, 3,4,5,6,7,8,9,0,11])






# *************************************************************Data structures and algorithm ends here********************************************************************************************************************