from collections import defaultdict

d= defaultdict(dict)
for x in range(2):
    d['B_'+str(x)]='name'
    print(d)
