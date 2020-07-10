class SampleClass:
    dog_name = "rat"

    def __init__(self, breed="New breed", name="lab"):
        self.breed = breed + ' name'
        self.name = name

    def bark(self, age):
        self.age = age
        print(f"WOOF! the age of the dog is {age} {self.breed}  {self.dog_name} {SampleClass.dog_name}")
        print(f":Address Book.{age}_QMenu")

    def sam_funct(self):
        print("funct with no argument")


# sam_obj = SampleClass(breed="Lab", name="sam")
# print(sam_obj.dog_name)
# sam_obj.bark(21)
# sam_obj1 = SampleClass(breed="als", name="Frankie")
# print(sam_obj1.name)
# sam_obj1.dog_name = "New name"
# print(sam_obj1.dog_name)
# sam_obj1.bark(20)
# print(sam_obj.age)
# print(sam_obj.dog_name)
# print(sam_obj1.dog_name)
# print(sam_obj1.dog_name)
# print(sam_obj1.breed)
# print(sam_obj1.dog_name)
# sam_obj1.dog_name = "New rat"
# print(SampleClass.dog_name)
#
# print(sam_obj1.dog_name)
# sam_obj1.sam_funct()
# sam_obj1.bark(21)
sam_obj4 = SampleClass(breed="new__", name="labbbb")
print(sam_obj4.breed)
print(sam_obj4.name)
print(sam_obj4.bark(23))
# print(sam_obj4.age)
# print(SampleClass.breed)
# print(SampleClass.bark(23))
