import sys
import re
import datetime
import time

regex = re.compile("(?<=(\[)).*?(?=-\d\d\d\d\])")

class pacman_package:
    def __init__(self, line):
        self.line = line
        tmp = regex.search(line).group(0)
        self._date = datetime.datetime.strptime(tmp, "%Y-%m-%dT%X")
    def date(self):
        return self._date.strftime("%c")

f = open("/var/log/pacman.log", "r")


for line in f:
    if re.search("upgraded", line):
        pkg = pacman_package(line)
        print(pkg.date())
