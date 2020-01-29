import pacman
import random
import string

tlist = []
for i in range(1,11):
    out = random.choice(string.ascii_lowercase) + "_test_class_" + random.choice(string.ascii_lowercase)
    tlist.append(t(out))

print(tlist)
tlist.sort(key=lambda x: x.name)
print(tlist)
