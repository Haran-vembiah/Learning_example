from collections import defaultdict

data = [(2010, 2), (2009, 4), (1989, 8), (2009, 7)]
d = defaultdict(list) #defaultdict to handles the missing key more about defaultdict(list) https://realpython.com/python-defaultdict/
for year,month in data:
    d[year].append(month)
print(d)

d=dict()
print(type(d))
for k,v in data:
    d[k] = v
print(d)


dict1 = {1:23}
print('For dir')
print(dir(dict1))

# list comprehension
d = {'ANIMAL' : ['CAT','DOG','FISH','HEDGEHOG']}
d_list = [[k,v] for k,value in d.items() for v in value]
print('by list comprehension')
print(d_list)

# Iteration over
d = {'ANIMAL' : ['CAT','DOG','FISH','HEDGEHOG']}
d_list = []
for key, values in d.items():
    for value in values:
        d_list.append([key, value])

d1 = {12:{'Name': 'John12', 'Age': '27', 'Sex': 'Male'}}
d2 = {13:{'Name': 'John13', 'Age': '27', 'Sex': 'Male'}}
d3 = {14:{'Name': 'John', 'Age': '27', 'Sex': 'Male'}}
d4 = {15:{'Name': 'John', 'Age': '27', 'Sex': 'Male'}}

print(d3)
print("---------------")

dic = defaultdict(dict)
dic['123'].update(d1) #Add the first dic inside the key '123'
dic['123'].update(d2) #Add the second dic inside the key '123'
dic['124'].update(d3)
dic['124'].update(d4)
# print(dic['123'][0])
# print(dic['123'][1])
print(dic)
for x in dic:
    print(x)
for x in dic['123']:
    print(f"Value of {x} is {dic['123'][x]}")
    for k,v in dic['123'][x].items():
        print(f"value of key is {k}")
        print(f"value of values is {v}")
    # print(y)
    # print(y)

print("-----------------")
# print(dic['123']['12']['Name'])
# for ids, backl in dic:
#     print(ids)
#     for src,trg in backl:
#         print(src)