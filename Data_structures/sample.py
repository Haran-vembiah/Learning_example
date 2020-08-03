from collections import defaultdict

d= defaultdict(dict)
for x in range(2):
    d['B_'+str(x)]='name'
    print(d)


list1 = [123,234,456,123,234,987,654]
print(list1)
list1 = list(set(list1))
print(list1)