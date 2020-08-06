from collections import defaultdict

lst1 = [1,2,3,4]
lst2 = [11,12]
print(lst1)
lst1.extend(lst2)
print(lst1)

dict1 = defaultdict(dict)
print(id(dict1))

kwars ={'dictname':dict1}
print(id(kwars['dictname']))
dict1.update({'name':'Haran','sex':'male'})
print(id(dict1))
print(kwars['dictname'])
print(id(kwars['dictname']))