import random

samp = [['Burette 1', '', 'MB/ACT_A1'], ['Burette 2', '', 'Not connected'], ['Burette 5', '', 'Not connected'],
        ['burette 3', '', 'Not connected'], ['burette 5', '', 'Not connected']]
if all('burette 15' not in sublist for sublist in samp):
    print('exist')
if any('burette 5' in sublist for sublist in samp):
    print('exist')

t = [[1, 2, 3], [4, 5, 6], [7], [8, 9]]
flat_list = [item for sublist in t for item in sublist]
print(flat_list)

print(sum(t, []))

sam_list = [1, 2, 3, 4, 5, 6]
print(sam_list)
sam_list1 = []
sam_list.append(7)
print(sam_list)
sam_list.insert(0, 0)
print(sam_list)
sam_list.remove(5)
print(sam_list)
popped = sam_list.pop()
print(popped)
print(sam_list)
sam_list.pop(3)
print(sam_list)
sam_list.sort()
print(sam_list)
sam_list.reverse()
print(sam_list)
sam_list.sort()
print(sam_list)
print(sam_list1)
sam_list1 = sam_list.copy()
print(sam_list1)

list1 = [1, 2, 3, 4, 5, 6, 7]
print('after del')
del list1[1]
print(list1)
sub_list = [2, 3, 5]
new_list = []
new_list = [x for x in list1 if x in sub_list]
print(new_list)

randonm_item = random.random()
print(randonm_item)

randonm_item1 = random.randint(1, 6)
print(randonm_item1)

leader = random.choice(sam_list)
print(leader)

ages = [5, 12, 17, 18, 24, 32]


def myFunc(x):
    if x < 17:
        return False
    else:
        return True


adults = filter(myFunc, ages)
for x in adults:
    print(x)

tup_sam = (1, 2, 3)
print(len(tup_sam))
print(tup_sam[1])
