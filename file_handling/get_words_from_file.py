import pandas as pd

flake8_report = open('flake8_report.txt', 'r')
reportlines = flake8_report.readlines()
error_code_list = []
error_text_list = []
filename = "Flake8_report.xlsx"
for reportline in reportlines:
    whole_report = reportline.split()
    error_code = whole_report[1]
    error_code_list.append(error_code)
    error_text = " "
    error_text = error_text.join(whole_report[2:])
    error_text_list.append(str(error_text))
    # print(error_code)
    # print(error_text)
sam = pd.DataFrame({
    'Error_code': error_code_list,
    'Error_text': error_text_list
})
with pd.ExcelWriter(filename) as writer:
    sam.to_excel(writer, sheet_name='Detiled_info', index=False)

flake8_report.close()

print(error_code_list)
