# Arch-Rollback - Development branch
The easy way to undo previous upgrades in Arch and other Linux Distributions that use the _pacman_ package manager.

# Dependencies
This program relies upon [Colorama](https://github.com/tartley/colorama) and Curses to work. Colorama can be installed from github or by running `pip install --user colorama`.

# Installation
Run `git clone https://github.com/CoralRocker/Arch-Rollback.git`. That's it!

# Usage -- Downgrader
Simply run `python UndoUpgrade.py` in the git directory. The program will run you through downgrading.

# Usage -- Package Selecter
Run `python SelectPackage.py` in the git directory. The package selecter is not finished yet and isn't actually useful, currently. Packages are sorted alphabetically according to their first initial.

# Options -- Downgrader
**Get package by upgrade** Sort packages to downgrade by the last time a package was upgraded with pacman, be it with `pacman -Syu` or `pacman -S`.

**Get package by time** Sort packages by time between upgrades. This means that is two packages were updated with separate commands but with a set amount of time of each other, both can still be downgraded.

**Print all packages** Simply prints information about found packages. Prints name, date upgraded, old version name, and new version name.

**Downgrade only specific packages** Allows you to select which packages to downgrade and which ones to keep the same. Simply enter numbers or a range of numbers corresponding to which packages to downgrade.

**Print Command** Prints a command which you can run to downgrade all selected packages, or all packages if you didn't select any

**Downgrade** Runs the pacman command to downgrade all selected packages.

# Options -- Package Selecter
**_spacebar_** Selects the currently highlighted package to be worked on

**_left_arrow_** Shifts to previous initial key.

**_right_arrow_** Shifts to next initial key.

**_down_arrow_** Shifts to next package in list.

**_up_arrow_** Shifts to previous package in list.

**j** Jump to a specific key. Enter the letter or number corresponding to the key to jump to it

**s** Select or deselect a range of packages. Enter the first index of the range, then the last index. The range is inclusive.
