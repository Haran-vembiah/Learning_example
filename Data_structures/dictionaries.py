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
print(dir(dict1))

# list comprehension
d = {'ANIMAL' : ['CAT','DOG','FISH','HEDGEHOG']}
d_list = [[k,v] for k,value in d.items() for v in value]
print(d_list)

# Iteration over
d = {'ANIMAL' : ['CAT','DOG','FISH','HEDGEHOG']}
d_list = []
for key, values in d.items():
    for value in values:
        d_list.append([key, value])

d1 = {12:{'Name': 'John', 'Age': '27', 'Sex': 'Male'}}
d2 = {13:{'Name': 'John', 'Age': '27', 'Sex': 'Male'}}
d3 = {14:{'Name': 'John', 'Age': '27', 'Sex': 'Male'}}
d4 = {15:{'Name': 'John', 'Age': '27', 'Sex': 'Male'}}

print(d3)
print("---------------")

dic = defaultdict(list)
dic['123'].append(d1) #Add the first dic inside the key '123'
dic['123'].append(d2) #Add the second dic inside the key '123'
dic['124'].append(d3)
dic['124'].append(d4)
print(dic['123'][0])
print(dic['123'][1])
print(dic)
print("-----------------")
# print(dic['123']['12']['Name'])
# for ids, backl in dic:
#     print(ids)
#     for src,trg in backl:
#         print(src)