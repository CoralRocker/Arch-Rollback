import sys
import re
import datetime
import time

log_file = "./pacman.log"

regex = re.compile("(?<=(\[)).*?(?=-\d\d\d\d\])")

class pacman_list:
    def __init__(self):
        self.pkgs = []
        self.NameRegex = re.compile("(?<=(upgraded ))[a-zA-z\d\-\_\.]+?(?= \()")
        self.VerRegex = re.compile("(?<=\()([\_a-zA-Z\d\.\-\+\:]+) -> ([\_a-zA-Z\d\.\-\+\:]+)(?=\))")

    def add(self, package):
        self.pkgs.append(package)

    def sort(self):
        pkg_date = self.pkgs[len(self.pkgs)-1]._date #datetime.datetime(1970, 1, 1, 0, 0, 0)
        good_list = []
        for pkg in reversed(self.pkgs):
            dif = pkg._date - pkg_date
            dif_min = dif.seconds / 60
            if dif_min < 150:
                good_list.append(pkg)
            elif dif_min > 150:
                break
            pkg_date = pkg._date
        self.pkgs = good_list
    def updatePackages(self):
        for pkg in self.pkgs:
            pkg.getName(self.NameRegex)
            pkg.getVer(self.VerRegex)
    def printPackages(self):
        for pkg in self.pkgs:
            print(f"{pkg.pkg_name} upgraded {pkg._date} {pkg.old_ver} to {pkg.new_ver}")

class pacman_package:
    def __init__(self, line):
        self.line = line
        tmp = regex.search(line).group(0)
        self._date = datetime.datetime.strptime(tmp, "%Y-%m-%dT%X")
    def date(self):
        return self._date.strftime("%c")
    def getName(self, regex):
        self.pkg_name = regex.search(self.line).group(0)
    def getVer(self, regex):
        self.old_ver = regex.search(self.line).group(1)
        self.new_ver = regex.search(self.line).group(2)

f = open(log_file, "r")

l = pacman_list()

for line in f:
    if re.search("upgraded", line):
        l.add(pacman_package(line))
        
l.sort()
l.updatePackages()
l.printPackages()
