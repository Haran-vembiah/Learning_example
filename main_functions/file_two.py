# Python module to import
from file_one import *

print("File two __name__ is set to: {}".format(__name__))


def function_three():
    print("Function three is executed")


if __name__ == "__main__":
    print("File two executed when ran directly")
    function_two()
else:
    print("File two executed when imported")
