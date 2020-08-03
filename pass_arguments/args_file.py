from collections import defaultdict
from pprint import pprint

from pass_arguments import param_pass

dict1 = defaultdict()

kwargs_pass = {
    'dict_name': dict1
}
pprint(kwargs_pass['dict_name'])

for num in range(0,2):
    val1 = param_pass.samp_funct(num,**kwargs_pass)

# pprint(kwargs_pass['dict_name'])
# print(id(kwargs_pass['dict_name']))
# print(val1)
# pprint(val1)
# print(id(val1))
# pprint(val1)