import json
from collections import defaultdict
from pprint import pprint

import pandas as pd

error_code_list = []
# file_name_list = []
error_text_list = []
code_text_dict = defaultdict(list)
f = open("flake_report_10022023_125053.json", "r")
# print(f.read())
loaded_flake8_report_json = json.loads(f.read())
print(type(loaded_flake8_report_json))
# print(loaded_json.items())
for filename, error_code_details in loaded_flake8_report_json.items():
    if error_code_details:
        for single_error_code_details in error_code_details:
            code_text_dict[single_error_code_details['code']][0] = single_error_code_details['text']
            
            # print(single_error_code_details['code'])
            if single_error_code_details['code'] not in error_code_list:
                error_code_list.append(single_error_code_details['code'])
            if single_error_code_details['text'] not in error_text_list:
                error_text_list.append(single_error_code_details['text'])
# print(error_code_list, end="")
# for i in error_code_list:
#     print(i)
print(f"length of code list {len(error_code_list)}")
print(f"length of text list {len(error_text_list)}")
pprint(code_text_dict)
filename = "Flake8_report_summary.xlsx"
sam = pd.DataFrame({
    'Error_code': error_code_list,
    'Error_text': error_text_list
})
with pd.ExcelWriter(filename) as writer:
    sam.to_excel(writer, sheet_name='Detiled_info', index=False)
