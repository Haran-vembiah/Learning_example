class Animal():
    def __init__(self):
        print("Object for Animal created")
    # def speak(self):
    #     raise NotImplementedError("Implement in the derived class")


class Dog(Animal):

    def __init__(self,name):
        self.name = name
    def speak(self):

        print(self.name + " says Woof")

class Cat():
    def __init__(self, name):
        self.name = name
    def speak(self):
        print(self.name + " says Meow")


my_dog = Dog("Lab")
my_cat = Cat("Lus")
print(my_dog.speak())
print(my_cat.speak())