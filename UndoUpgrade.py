import re
import datetime
import time
from os import listdir
from os.path import isfile, join
import subprocess
import configparser
from pacman import pacman_list

def repeatingInput(prompt, default=False):
    while True:
        out = input(prompt)
        if len(out) != 0 or default!=False:
            return (out if len(out) != 0 else default)

log_file = "/var/log/pacman.log"
cache_dir = "/var/cache/pacman/pkg"
time_difference = 15

config = configparser.ConfigParser()
config.read("downgrader.conf")


log_file = config["DEFAULT"]["LogFile"]
cache_dir = config["DEFAULT"]["CacheDir"]
time_difference = int(config["DEFAULT"]["AllowableDifference"])


f = open(log_file, "r")

l = pacman_list()

for line in f:
    if re.search("upgraded", line):
        l.cadd(line)

l.sort()
l.updatePackages()
print("Packages Found and Sorted.")
print_if = repeatingInput("Print all packages? (y/N) ", 'n')[0].lower()
if print_if == "y":
    l.printFiles()
print_if = repeatingInput("Downgrade only specific packages? (y/N) ", 'n')[0].lower()
if print_if == "y":
    l.printFiles(True)
    print("Separate with commas or spaces. May use ranges (Num1-Num2 inclusive) or singular numbers.")
    print("EX: 1-23 34, 37-43")
    instr = repeatingInput("Enter requested numbers: ") 
    l.getPackages(instr)
    instr = repeatingInput("Print command? (Y/n) ", 'y')[0].lower()
    if instr == 'y':
        l.printCommand(True, True)


