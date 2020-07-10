
print("sample code")
name = 'satring'
for i in name:
    print(i)

my_list = [1,2,3,4,5,6]
for x in my_list:
    if (x==3):
        print(f"got {x}")
    else:
        print(x)

# my_file = open("test.txt", mode='r+')
# cont = my_file.readlines()
# for i in cont:
#     print(i)
# my_file.write("\n new line")
# cont = my_file.readlines()
# for i in cont:
#     print(i)


# Examples for *args and **Kwargs
def my_funct(*args):
    '''
    To demonstrate the usage of *args as parameter, taken as tuple
    '''
    
    for x in args:
        print(x)
        
def my_funct1(**kwargs):
    '''
    To demonstrate the usage of **kwargs as parameter, taken as dictionary
    '''
    for values_ in kwargs.values():
        print(f"Values are {values_}")
    for keys_ in kwargs.keys():
        print(f"Keys are:{keys_}")

# Calling the function using *args and **kwargs
print(help(my_funct))
my_funct('name','first_name','last_name')
print(help(my_funct1))
my_funct1(name='value', name1 = 'value2')




# To demonstrate the map function by iterating dictionary
my_dict_for_map = {'key1':'v1', 'key2':'value2','key3':'value3'}
def my_funct_map_dict(names):
    print(type(names)) #It retuns the tuple
    # print(type(names[0]))
    print(f"Key value is {names[0]}") #Through inndex of the tuple
    print(f"Value is {names[1]}") #Through inndex of the tuple


list(map(my_funct_map_dict,my_dict_for_map.items()))

# To demonstrate the map function by iterating list
my_list_for_map = [1,2,3,4,5]
def my_funct_map_list(nums):
    # print(type(nums)) 
    # print(type(names[0]))
    print(f"Value {nums} multiply by 2 is {nums *2}")


list(map(my_funct_map_list,my_list_for_map))



# To demonstrate the filter function
def demo_filter_funct(names):
    return names[0]=='a'
    # print(names)
        # return names
nam_list = ['aravind','bala','aakaash','kalai']
print(list(filter(demo_filter_funct,nam_list)))
# demo_filter_funct(nam_list)

def square_fun(num): return num *2
print(square_fun(3))

# Using lambda function
num_sqr = lambda num:num*2
print(num_sqr(3))

my_nums= [1,2,3]
print(list(map(lambda num:num*2, my_nums)))

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



