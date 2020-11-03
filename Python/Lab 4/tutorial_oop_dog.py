class Dog():
    name = ""
    age = 0
    __breed = None

    def __init__(self, dog_name, dog_age, dog_breed):
        self.name = dog_name
        self.age = dog_age
        self.__breed = dog_breed

    def speak(self, sound):
        print(self.name, "says", sound)

    def run(self, speed):
        print(self.name, "runs", speed, "mph")

    def description(self):
        print(self.name, "is a", self.age, "year old", self.__breed)

    def define_buddy(self,buddy):
        self.buddy = buddy
        buddy.buddy = self

scout = Dog("Scout", 2, "Belgian Malinois")
print(scout)
print(scout.name)
print(scout.age)
scout.speak("woof")
scout.description()

# Question 1: Printing out scout shows information about the instance we created. It shows its location,
# what class definition it uses, and its memory address.

# Question 2: If we were to print out scout.__breed, an error would occur. Breed is a private variable, meaning
# can only be accessed inside the Dog class. Since we are trying to access breed in main, an error will occur since it is
# private variable

# Question 3:
skippy = Dog("Skippy", 5, "Golden Retriever")
scout.define_buddy(skippy)
scout.buddy.description()
