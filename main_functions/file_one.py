# Python module to execute
# from file_two import *

print("File one __name__ is set to: {}".format(__name__))


def function_one():
    print("Function one is executed")


def function_two():
    print("Function two is executed")


def funct2(param1=None, param2=None):
    print(f'value is {c} and {d}')


if __name__ == "__main__":
    c = 1
    d = 2
    print("File one executed when ran directly")
    function_two()
    # function_three()
    funct2(param1=c, param2=d)
else:
    print("File one executed when imported")
