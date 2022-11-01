s1 = set()
s1 = (1, 2, 3, 4)
s2 = set()
s2 = (2, 3, 4, 5)
s1_diff = sorted(set(s1).difference(set(s2)))
print(s1_diff)

s2_diff = sorted(set(s2).difference(set(s1)))
print(s2_diff)

s_equals = set(s1) == set(s2)
print(s_equals)

equal_set = sorted(set(s1).intersection(set(s2)))
print('is sets are equal', equal_set)
print(len(equal_set))
