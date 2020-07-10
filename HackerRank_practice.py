# Hello World
"""
input_string = input()
print('Hello, World.')
print(input_string)
"""
# ====================================================

# Data types
'''
i = 10
d = 2.00
s = "hacker rank"
num_var = int(input("Enter value for j:\n"))
float_num = float(input("\nEnter a float value:"))
str_var = input("Enter a string:")
print("Addition of two numbers", i + num_var)
print("Addition of two numbers", d + float_num)
print("Addition of two numbers", s + str_var)
'''
# =====================================================
# Operators
import math
import os
import random
import re
import sys

# Complete the solve function below.
# def solve(meal_cost, tip_percent, tax_percent):
#     tip = meal_cost * (tip_percent / 100)
#     tax = meal_cost * (tax_percent / 100)
#     total_meal_cost = meal_cost + tip + tax
#     print(round(total_meal_cost))
#
#
# if __name__ == '__main__':
#     meal_cost = float(input())
#
#     tip_percent = int(input())
#
#     tax_percent = int(input())
#
#     solve(meal_cost, tip_percent, tax_percent)
# =====================================================

# Conditional statements
# If  is odd, print Weird
# If  is even and in the inclusive range of 2 to 5, print Not Weird
# If  is even and in the inclusive range of 6 to 20, print Weird
# If  is even and greater than 20, print Not Weird
# Complete the stub code provided in your editor to print whether or not  is weird.
# import math
# import os
# import random
# import re
# import sys
#
# if __name__ == '__main__':
#     N = int(input())
#     if N in range(1, 101):
#         if N % 2 != 0:
#             print("Weird")
#         elif (N % 2 == 0) and (2 <= N <= 5):
#             print("Not Weird")
#         elif (N % 2 == 0) and (6 <= N <= 20):
#             print("Weird")
#         elif (N % 2 == 0) and (N > 20):
#             print("Not Weird")
#         else:
#             print("Other case")
#     else:
#         print("Enter value between 1 to 100")
# ==============================================================
# class and instance
'''
class Person:
    age = None

    def __init__(self, initialAge):
        if initialAge < 0:
            self.age = 0
            print("Age is not valid, setting age to 0.")
        else:
            self.age = initialAge
        # Add some more code to run some checks on initialAge

    def amIOld(self):
        # Do some computations in here and print out the correct statement to the console
        if self.age < 13:
            print("You are young.")
        elif 13 <= self.age < 18:
            print("You are a teenager.")
        else:
            print("You are old.")

    def yearPasses(self):
        # Increment the age of the person in here
        self.age += 1


t = int(input())
for i in range(0, t):
    age = int(input())
    p = Person(age)
    p.amIOld()
    for j in range(0, 3):
        p.yearPasses()
    p.amIOld()
    print("")
'''
# ========================================================

# Loops
'''
import math
import os
import random
import re
import sys

if __name__ == '__main__':
    n = int(input())
    for i in range(1, 11):
        # print('{0} x {1} = {prod}'.format(n, i, prod=n * i))
        print(f"{n} x {i} = {n*i}")
'''
# =================================================================
# Review, Printing the even and odd index in same line for the given string
'''def review(s):
    for x in range(0, len(s), 2):
        print(s[x],end='') #Here the end ='' prints in the same line instead of printing in a new line
    print(" ",end='')
    for y in range(1, len(s), 2):
        print(s[y],end="")
    print(" ")


t = int(input())
for i in range(0, t):
    s = list(input())
    review(s)
'''
# =========================================================
# Arrays
'''
t = int(input())
# list_a = list(map(int, input().split(' '))) # Takes a single line input as list
# print(list_a)
# print(list_a[::-1])
for x in list_a[::-1]:
    print(x, end=' ')
'''

# ============================================================
# Dictionaries and maps

'''
my_dict = {}
t = int(input())
for x in range(0, t):
    user_input = input()
    key, value = user_input.split(" ")  # Getting input for dictionary item(space seperated)
    my_dict[key] = int(value)
try:
    while True:
        query = None
        query = input()
        if query in my_dict.keys():
            print(f"{query}={my_dict[query]}")
        else:
            print("Not found")
except EOFError as e:   # EOFError exception
    print(end="")
'''
# ===========================================================================
# Factorial
import math
import os
import random
import re
import sys

# Complete the factorial function below.
'''
import math
import os
import random
import re
import sys

# Complete the factorial function below.
def factorial(n):
    if n == 1:
        return 1
    else:
        return n * factorial(n-1)

if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')
    n = int(input())
    result = factorial(n)
    fptr.write(str(result) + '\n')
    fptr.close()
'''

# =================================================================
# Task
# Given a base- integer, , convert it to binary (base-). Then find and print the base- integer denoting the maximum number of consecutive 's in 's binary representation.
'''
import math
import os
import random
import re
import sys

if __name__ == '__main__':
    n = int(input())
    bin_list = [i for i in list(f'{n:b}')]  # Getting a binary value of n as list
    print(bin_list)
    count = 0
    result = 0
    for x in range(0, len(bin_list)):
        if bin_list[x] == '0':    # By using simple method
            count = 0
        else:
        # while x != 0:
        #     x = (x & (x << 1))    # By using bitwise operator
            count += 1
            result = max(count, result) #It holds the max value and compares with the last max value
    print(result)
'''
# ============================================================================  This is not started yet
# 2D Array
# Calculate the hourglass sum for every hourglass in , then print the maximum hourglass sum.
'''
n = int(input())
arr_list = []
# Getting numbers in to the array
for _ in range(0, n):
    arr_list.append(list(map(int, input().split())))
print(arr_list)
# Adding the values of hour glass
start_row_index = 0
start_col_index = 0
mid_row_start = 1
mid_col = 1
loop_count = 0
# return_value = 0
while loop_count <= (n - 2) ** 2:
    if start_row_index > n - 3:  # Checks whether it exceeds the possible starting index of row for given n*n matrix
        break
    total_value = 0
    print(f"Index : [{start_row_index},{start_col_index}]")
    print(f"mid_col is {mid_col}")
    print(f"Index : [{start_row_index + 2},{start_col_index}]")
    print("================================================")
    total_value += arr_list[mid_row_start][mid_col]  # Adding the middle row(Single value)
    for _ in range(0, 3):
        total_value += arr_list[start_row_index][start_col_index]  # Adding the First row(Three values)
        total_value += arr_list[start_row_index + 2][start_col_index]  # Adding the Third row(Three values)
        start_col_index += 1  # Incrementing the 2nd index by 1
        # print(f"Total value is {total_value}")
    if loop_count == 0:
        return_value = total_value
    print(f"Total value is {total_value}")
    return_value = max(total_value, return_value)  # Returns the max value on all the executed loops
    if start_col_index > n - 2 and mid_col > n - 3:  # Checks whether it exceeds the possible starting index of col and mid_col for given n*n matrix
        start_col_index = 0
        mid_col = 1
        start_row_index += 1
        mid_row_start += 1
    else:
        start_col_index -= 2
        mid_col += 1
    loop_count += 1  # Incrementing loop count by 1

print(return_value)

'''

# ============================================================================================
# Inheritance example
'''
class Person:
    def __init__(self, fn, ln, idNumber):
        self.firstName = fn
        self.lastName = ln
        self.idNumber = idNumber

    def printPerson(self):
        print("Name:", self.lastName + ",", self.firstName)
        print("ID:", self.idNumber)


class Student(Person):
    #   Class Constructor

    #
    #   Parameters:
    #   firstName - A string denoting the Person's first name.
    #   lastName - A string denoting the Person's last name.
    #   id - An integer denoting the Person's ID number.
    #   scores - An array of integers denoting the Person's test scores.
    #
    # Write your constructor here
    def __init__(self, fn, ln, idnumber, scores):
        self.firstName = fn
        self.lastName = ln
        self.idNumber = idnumber
        self.scores = scores

    #   Function Name: calculate
    #   Return: A character denoting the grade.
    #
    # Write your function here
    def calculate(self):
        # self.scores = scores_list
        total = 0
        avg = 0
        for mark in range(0, len(self.scores)):
            total += self.scores[mark]
        avg = total / len(self.scores)
        if 90 <= avg <= 100:
            return "O"
        elif 80 <= avg <= 90:
            return "E"
        elif 70 <= avg <= 80:
            return "A"
        elif 55 <= avg <= 70:
            return "P"
        elif 40 <= avg <= 55:
            return "D"
        else:
            return "T"


line = input().split()
firstName = line[0]
lastName = line[1]
idNum = line[2]
numScores = int(input())  # not needed for Python
scores = list(map(int, input().split()))
s = Student(firstName, lastName, idNum, scores)
s.printPerson()
print("Grade:", s.calculate())
'''
# =============================================================================================
