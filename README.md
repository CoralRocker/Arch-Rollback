# Arch-Rollback - Develop Branch
The easy way to undo previous upgrades in Arch and other Linux Distributions that use the _pacman_ package manager.

This branch is liable to be unusable at any given moment since it is the branch that is being actively worked on. Stable "releases" will be in the master branch. 

# Dependencies

This program relies upon [Colorama](https://github.com/tartley/colorama) and Curses to work. Colorama can be installed from github or by running `pip install --user colorama`.


# Installation
Run `git clone https://github.com/CoralRocker/Arch-Rollback.git`. That's it!

# API Documentation

# [pacman.py](pacman.py)

### pacman_list class
| Method Name | Parameters | What It Does |
|:---:|---|---|
| \_\_init__ | none | Sets up the list to be ready to store package information |
| cadd | line | Given _line_ from the pacman log file, will create a new package with the information and add it to the package list
| sort | none | Sorts complete list of packages to contain only packages updated within 30 minutes of each other
| updatePackages| none | Calls on all sorted packages to update their information
| printPackages | none | Prints packages to terminal in a pretty way. Tells when it was last updated and what versions were affected.
| appendSelected | addendum | Adds _addendum_ to list of selected packages. _Addendum_ may be a list or a single package 
