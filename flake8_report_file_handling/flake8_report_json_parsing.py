import json
from collections import defaultdict

import pandas as pd

error_code_list = []
error_text_list = []
error_Occurrence_list = []
code_text_list_dict = defaultdict(list)
code_text_dict = {}

# Replace the name of current report to get the updated data
f = open("flake_report_10022023_125053.json", "r")
# print(f.read())
loaded_flake8_report_json = json.loads(f.read())
print(type(loaded_flake8_report_json))
# print(loaded_json.items())
for filename, error_code_details in loaded_flake8_report_json.items():
    if error_code_details:
        for single_error_code_details in error_code_details:
            code_text_list_dict[single_error_code_details['code']].append(single_error_code_details['text'])
            code_text_dict[single_error_code_details['code']] = single_error_code_details['text']

            # code_text_dict[single_error_code_details['code']][1] = "single_error_code_details['text']"

            # # print(single_error_code_details['code'])
            # if single_error_code_details['code'] not in error_code_list:
            #     error_code_list.append(single_error_code_details['code'])
            # if single_error_code_details['text'] not in error_text_list:
            #     error_text_list.append(single_error_code_details['text'])
# print(error_code_list, end="")
# for i in error_code_list:
#     print(i)
# print(f"length of code list {len(error_code_list)}")
# print(f"length of text list {len(error_text_list)}")
# pprint(code_text_list_dict)
for code, text_list in code_text_list_dict.items():
    # print(code)
    error_code_list.append(code)
    # print(len(text_list))
    error_text_list.append(code_text_dict[code])
    error_Occurrence_list.append(len(text_list))
    # code_text_count_dict[code].append(len(text_list))


# print(code_text_dict)
# print(error_code_list)
# print(len(error_code_list))
# print(error_text_list)
# print(len(error_text_list))
# print(error_occurance_list)
# print(len(error_occurance_list))

filename = "Flake8_report_summary.xlsx"
sam = pd.DataFrame({
    'Error_code': error_code_list,
    'Error_text': error_text_list,
    'Occurrence': error_Occurrence_list
})
with pd.ExcelWriter(filename) as writer:
    sam.to_excel(writer, sheet_name='Detiled_info', index=False)
