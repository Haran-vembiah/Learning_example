def samp_funct(num, **kwargs):
    dict2 = kwargs['dict_name']
    # print('id of ori dict',id(kwargs['dict_name']))
    # print('id of reassigned',id(dict2))
    dict3 = dict(kwargs['dict_name'].items())
    # print('id of created dict',id(dict3),dict(dict3))
    print(dict3)
    print(id(dict3))
    dict3[num] = num + 1

    # print(dict3)

    return dict3