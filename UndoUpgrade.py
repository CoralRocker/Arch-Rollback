from colorama import Fore
import re
import configparser
from pacman import pacman_list


# Simple method to get output from some prompts
def repeatingInput(prompt, default=False):
    while True:
        out = input(prompt)
        if len(out) != 0 or default!=False:
            return (out if len(out) != 0 else default)

# Config file parsing
config = configparser.ConfigParser()
config.read("downgrader.conf")

log_file = config["DEFAULT"]["LogFile"] or "/var/log/pacman.log"
cache_dir = config["DEFAULT"]["CacheDir"] or "/var/cache/pacman/pkg"
time_difference = int(config["DEFAULT"]["AllowableDifference"]) | 15
get_by_upgrade = (True if config["DEFAULT"]["GetByUpgrade"].lower() == "true" else False) | False

f = open(log_file, "r")

l = pacman_list()

'''
Intro Text
'''

instr = repeatingInput(f"Get packages by upgrade? Alternative is by time. {Fore.GREEN}{'(Y/n)' if get_by_upgrade else '(y/N)'}{Fore.RESET} ", 'y' if get_by_upgrade else 'n')[0].lower()
if instr == 'y':
    get_by_upgrade = True
else:
    get_by_upgrade = False
    instr = repeatingInput(f"Current time allowed between upgraded packages is {time_difference} minutes. Change? {Fore.GREEN}(y/N){Fore.RESET} ", 'n')[0].lower()
    if instr == 'y':
        time_difference = int(repeatingInput("Enter time: ",str(time_difference)))

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
    l.sort()
'''
Run package discovery methods
'''
l.updatePackages()
print("Packages Found and Sorted.")

'''
User options and input
'''

# Display Packages
print_if = repeatingInput(f"Print all packages? {Fore.GREEN}(y/N){Fore.RESET} ", 'n')[0].lower()
if print_if == "y":
    l.printFiles()

# Specific package downgrading
print_if = repeatingInput(f"Downgrade only specific packages? {Fore.GREEN}(y/N){Fore.RESET} ", 'n')[0].lower()
if print_if == "y":
    l.printFiles(True)
    print("Separate with commas or spaces. May use ranges (Num1-Num2 inclusive) or singular numbers.")
    print("EX: 1-23 34, 37-43")
    instr = repeatingInput("Enter requested numbers: ") 
    l.getPackages(instr)
    

# Print command
instr = repeatingInput(f"Print command? {Fore.GREEN}(Y/n){Fore.RESET} ", 'y')[0].lower()
if instr == 'y':
    l.printCommand(True)

# TODO Make program downgrade by itself...
instr = repeatingInput(f"Downgrade? (Y/n) ", 'y')[0].lower()
if instr == 'y':
    l.downgrade()

