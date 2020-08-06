from collections import defaultdict
from pprint import pprint

'''
# ============== Writing data with intermediate dict ================
back_req = defaultdict(dict) #Declaration of main dictionary
for x in range(2):
    backlog = defaultdict(dict) # declaration of Backlog dict
    req = defaultdict(dict) # declaration of req dict
    # Writing content to Backlog dictionary
    backlog['Backlog'+str(x)]['Name']= 'John'
    backlog['Backlog'+str(x)]['Age']= '23'
    backlog['Backlog'+str(x)]['sex']= 'Male'
    print(backlog)
    # Writing content to req dictionary
    req['Req'+str(x)]['Name']= 'John'
    req['Req'+str(x)]['Age']= '23'
    req['Req'+str(x)]['sex']= 'Male'
    print(req)
    # Writing data to main dictionary
    back_req['backlog'+str(x)+'-req'+str(x)].update(backlog)
    back_req['backlog'+str(x)+'-req'+str(x)].update(req)
print(back_req)
# ======================================================================
'''

# ============== try writing data in a loop - single step=================
single_d = defaultdict(dict)
for x in range(2):
    single_d['backlog'+str(x)+'-req'+str(x)]['Backlog'+str(x)] = {'Name': 'John12', 'Age': '27', 'Sex': 'Male'}
    single_d['backlog'+str(x)+'-req'+str(x)]['Req'+str(x)] = {'Name': 'John', 'Age': '27', 'Sex': 'Mal'}


print(single_d)
# =============================================================


for x in single_d:
    print(x)
    for x1 in single_d[x]:
        print(f"x1: {x1}")
        print(single_d[x][x1])
        print(single_d[x][x1]['Name'])


print("-----------------")
dict2 = {'name':'haran'}

dict_sample = {31441: {12345:
                   {'changes_after_resolved': 'No_changes',
                    'changes_after_closed': 'No_changes',
                    'linked_backlog': 27429}
               }}

print(dict_sample)
dict_sample[31441][12345].update({'dasda':'fsdfsd','fff':'fdsfsdfsd'})
print(dict_sample)
dict2.update(dict_sample)
print(dict2)
pprint(dict2)

