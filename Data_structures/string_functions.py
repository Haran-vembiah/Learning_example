import pydoc
import string

sam_ = "AnaChemProjects\\G5\\Titration\\KF\\SW\\Orion"
sam_list = sam_.split('\\')
print(sam_list)
name = '30319-27249'
print(name)
backlog_req = name.split('-')
print(backlog_req)
print(type(backlog_req))

print(backlog_req[0])

param_value = "Burette(s) 4"
new_value = param_value.rstrip("(s) 4")
print(new_value)
new_str = param_value.split(" ")
print(new_str)

str1 = "welcome to python"
help(str1)
attrs = dir(str1)
for attr in attrs:
    if attr == '__doc__':
        # help(attr)
        print("Type: ", type(help(attr)))

print(str1.upper())
print(str1.title())
print(str1.replace('python', 'Java'))
print(str1.find('c'))
str_list = str1.split(" ")
print(str_list)
str_new = '-'
print(str_new.join(str_list))

pydoc.render_doc(string, renderer=pydoc.plaintext)
print('sd')
a = "ABCDCDCD"
sub_ = "CDC"


def count_substring(string, sub_string):
    count = 0
    for i in range(len(string)):
        if string[i:].startswith(sub_string):
            count += 1
    return count


print("count is: ", count_substring(a, sub_))
