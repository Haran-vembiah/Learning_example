def new_dec_funct(original_funct):
    def wrap_funct():
        print("Before original function")
        original_funct()
        print("After original function")

    return wrap_funct


@new_dec_funct
def ori_funct():
    print("I need to be decorated")
    print("This is from the decorator function")


ori_funct()

# Contents in ur code_sample.py
