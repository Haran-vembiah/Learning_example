test_case_list = [
    {"taf_tc_id": (2, 2),  # A tuple as (tc_id, tc_order), is the new key
     "ado_tc_id": "33333",
     "tc_title": "Existing Test Case",
     "parent_taf_ts_id": 51,
     "parent_ado_ts_id": "None"},
    {"taf_tc_id": (5, 11),
     "ado_tc_id": None,
     "tc_title": "New Test Case",
     "parent_taf_ts_id": 52,
     "parent_ado_ts_id": "None"},
    {"taf_tc_id": (6, 12),
     "ado_tc_id": None,
     "tc_title": "New Test Case1",
     "parent_taf_ts_id": 523,
     "parent_ado_ts_id": "None"}
]

new_dict = []
new_dict1 = {}
new_tuple_list = []

# new_dict2 = defaultdict()
inc = 1
for tc in test_case_list:
    new_dict.append({tc['taf_tc_id']: str(inc),
                     tc['tc_title']: str(inc)})
    new_dict1.update({tc['taf_tc_id']: str(inc)})
    new_tuple_list.append((tc['taf_tc_id'], tc['tc_title'], str(inc)))
    # new_dict.append({new_dict[tc['taf_tc_id']]: inc})
    inc = inc + 1

print(new_dict)
print(new_dict1)
print(new_tuple_list)

for taf, tc in new_dict1.items():
    print(taf)
    print(tc)
