import re
import datetime
import time
from os import listdir
from os.path import isfile, join
import subprocess
import configparser
from pacman import pacman_list


# Simple method to get output from some prompts
def repeatingInput(prompt, default=False):
    while True:
        out = input(prompt)
        if len(out) != 0 or default!=False:
            return (out if len(out) != 0 else default)

# Config file parsing
log_file = "/var/log/pacman.log"
cache_dir = "/var/cache/pacman/pkg"
time_difference = 15

config = configparser.ConfigParser()
config.read("downgrader.conf")

log_file = config["DEFAULT"]["LogFile"]
cache_dir = config["DEFAULT"]["CacheDir"]
time_difference = int(config["DEFAULT"]["AllowableDifference"])
get_by_upgrade = (True if config["DEFAULT"]["GetByUpgrade"].lower() == "true" else False) | False

f = open(log_file, "r")

l = pacman_list()

'''
Intro Text
'''

instr = repeatingInput(f"Get packages by upgrade? Alternative is by time. {'(Y/n)' if get_by_upgrade else '(y/N)'} ", 'y' if get_by_upgrade else 'n')
if instr == 'y':
    get_by_upgrade = True
else:
    get_by_upgrade = False


'''
Get information from log file in one of two ways
'''
# By upgrade, only grabs the upgrades from one pacman run
if get_by_upgrade:
    tmprgx = re.compile("\[PACMAN\] Running \'pacman \-S")
    upgraded = False
    for line in reversed(list(f)):
        if re.search("upgraded", line):
            upgraded = True
            l.cadd(line)
        if upgraded and tmprgx.search(line):
                break
# Or by time, grabs every line, and is then sorted by time with the pacman_list.sort() function Takes significantly more time...
else:
    for line in f:
        if re.search("upgraded", line):
            l.cadd(line)

'''
Run package list discovery methods
'''
l.sort()
l.updatePackages()
print("Packages Found and Sorted.")

'''
User options and input
'''

# Display Packages
print_if = repeatingInput("Print all packages? (y/N) ", 'n')[0].lower()
if print_if == "y":
    l.printFiles()

# Specific package downgrading
print_if = repeatingInput("Downgrade only specific packages? (y/N) ", 'n')[0].lower()
if print_if == "y":
    l.printFiles(True)
    print("Separate with commas or spaces. May use ranges (Num1-Num2 inclusive) or singular numbers.")
    print("EX: 1-23 34, 37-43")
    instr = repeatingInput("Enter requested numbers: ") 
    l.getPackages(instr)
    

# Print command
instr = repeatingInput("Print command? (Y/n) ", 'y')[0].lower()
if instr == 'y':
    l.printCommand(True)

# TODO Make program downgrade by itself...


