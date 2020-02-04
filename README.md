# Arch-Rollback
The easy way to undo previous upgrades in Arch and other Linux Distributions that use the _pacman_ package manager.

# Dependencies
This program relies upon [Colorama](https://github.com/tartley/colorama) to work correctly. You can install Colorama from github or simply run  `pip install --user colorama`.

# Installation
Run `git clone https://github.com/CoralRocker/Arch-Rollback.git`. That's it!


# Usage
Simply run `python UndoUpgrade.py` in the git directory. The program will run you through downgrading.

# Options
**Get package by upgrade** Sort packages to downgrade by the last time a package was upgraded with pacman, be it with `pacman -Syu` or `pacman -S`.

**Get package by time** Sort packages by time between upgrades. This means that is two packages were updated with separate commands but with a set amount of time of each other, both can still be downgraded.

**Print all packages** Simply prints information about found packages. Prints name, date upgraded, old version name, and new version name.

**Downgrade only specific packages** Allows you to select which packages to downgrade and which ones to keep the same. Simply enter numbers or a range of numbers corresponding to which packages to downgrade.

**Print Command** Prints a command which you can run to downgrade all selected packages, or all packages if you didn't select any

**Downgrade** Runs the pacman command to downgrade all selected packages.
