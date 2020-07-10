class Difference:
    def __init__(self, a):
        self.__elements = a

    # Add your code here
    def computeDifference(self):
        # count = 0
        start_index = 0
        maximumDifference = 0
        sorted_elements = sorted(self.__elements)
        self.maximumDifference = abs(sorted_elements[start_index] - sorted_elements[int(_) - 1])
# End of Difference class

_ = input()
a = [int(e) for e in input().split(' ')]

d = Difference(a)
d.computeDifference()

print(d.maximumDifference)