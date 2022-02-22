import json

with open("demo.json", 'r') as f:
    loaded_json = json.loads(f.read())


    # for x in loaded_json:
    #     # print(loaded_json[x])
    #     for y in loaded_json[x]:
    #         # print(y)
    #         print(loaded_json[x][y])
    def myprint(d):
        for k, v in d.items():
            if type(v) == dict:
                print(k)
                myprint(v)
            else:
                print(k, v)


    myprint(loaded_json)
# # JSON file
# f = open('demo.json', "r")
#
# # Reading from file
# data = json.loads(f.read())
#
# # Iterating through the json
# # list
# for i in data['widget']:
#     print(i)
#
# # Closing file
# f.close()
