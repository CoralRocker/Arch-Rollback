import random
import string

class test:
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return "Test Class: %s" % (self.name)

tlist = []

for i in range(1, 11):
    name = random.choice(string.ascii_lowercase) + "name" + str(i)
    tlist.append(test(name))

print(tlist)
