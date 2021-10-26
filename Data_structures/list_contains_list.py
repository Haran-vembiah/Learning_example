# Program to check the list contains elements of another list

# List1
List1 = ['python', 'javascript', 'csharp1', 'go', 'c', 'c++']


# List2
List2 = ['csharp1', 'go', 'python']

# check = all(item in List1 for item in List2)
if all(item in List1 for item in List2):
    print("matched")

# if check is True:
#     print("The list {} contains all elements of the list {}".format(List1, List2))
# else:
#     print("No, List1 doesn't have all elements of the List2.")


list3 =[]
list3.insert(0,'ddfd')
list3.insert(1,'dffd')
print(list3)