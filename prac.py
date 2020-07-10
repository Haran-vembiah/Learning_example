
grocery_list = ["fish", "tomato", 'apples']
print('fish' in grocery_list)
grocery_dict = {"fish": 1, "tomato": 6, 'apples': 3}
print('fish' in grocery_dict.keys())
print(6 in grocery_dict.values())

name = "John"
age = 17
# Check if name is "Ellis" or it's not true that name equal "John" and he is 17 years old at the same time.
print(name == "Ellis" or not (name == 'John' and age == 17))

# Difference of "is" and "=="
list1 = []
list2 = []
list3 = list1
print("To validate the is operator")
print(list1 is list2) #Returns False since it refers the diff references.
print(list3 is list1) #Returns True since it refers the same reference
print("To validate the == operator")
print(list1 == list2) #Returns True since the values are same even it refers the diff references.
print(list3 == list1) #Returns True since the values are same and also it refers the same reference

tasks = ['task1', 'task2']
if (len(tasks)==0):
    print("Empty")
else:
    print("Not empty")

helo_world = "Hello world"
length = 0
for x in helo_world:
    length+=1

print(len(helo_world)== length)

square = 0
number = 1

while(number<10):
    square = number ** 2
    print(square)
    number += 1

zoo = ["lion", 'tiger', 'elephant']
while True:                         # this condition cannot possibly be false
    animal = zoo.pop()       # extract one element from the list end
    print(animal)
    if animal is 'elephant':
        break   # exit loop
    print("After break")

for x in range(10):
    if x%2==0:
        continue
    print(f"Value is {x}" )

def fib(n):
    """This is documentation string for function. It'll be available by fib.__doc__()
    Return a list containing the Fibonacci series up to n."""
    result = []
    a = 1
    b = 1
    while a < n:
        result.append(a)
        tmp_var = b
        b = a + b
        a = tmp_var
    return result

print(fib(10))



def swap_fun(a=10,b=20):
    tmp_var = a
    a = b
    b = tmp_var
    return (a,b)
print(swap_fun(30,40))

def hello(subject,name= "haran"):
    print("Hello %s! My name is %s" % (subject, name))

hello("PyCharm", "Jane")    # call 'hello' function with "PyCharm as a subject parameter and "Jane" as a name
hello("PyCharm")            # call 'hello' function with "PyCharm as a subject parameter and default value for the name


class Complex:
    def create(self, real_part, imag_part):
        self.r = real_part
        self.i = imag_part
        print(self.r)
class Calculator:
    current = 0

    def add(self, amount):
        self.current += amount

    def get_current(self):
        return self.current

com = Complex()
calc = Calculator()
com.create(10,20)
calc.add(20)
print(calc.get_current())
calc.current = 35
print(calc.get_current())

from datetime import date
print(date.today())

from datetime import datetime
print(datetime.today())

class Sample1():
    def __init__(self):
        print("Class executed")
    def sam(self):
        print("Second sample")

s = Sample1()

class SamClass:
    def __init__(self,name):
        self.name = name
    def ret_name(self):
        return self.name
samc = SamClass("Haran")
print(samc.ret_name())

firstname = "   Haran         "
print(firstname.lstrip())
print(firstname.rstrip())







