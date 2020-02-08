# Arch-Rollback
The easy way to undo previous upgrades in Arch and other Linux Distributions that use the _pacman_ package manager.

# Dependencies

This program relies upon [Colorama](https://github.com/tartley/colorama) and Curses to work. Colorama can be installed from github or by running `pip install --user colorama`.


# Installation
Run `git clone https://github.com/CoralRocker/Arch-Rollback.git`. That's it!

# Usage -- Downgrader
Simply run `python UndoUpgrade.py` in the git directory. The program will run you through downgrading.

# Usage -- Package Selecter
Run `python SelectPackage.py` in the git directory. The package selecter is finally working! The UI is not finished yet, as I think that there's a few things I can do to improve it still, and there may be bugs, but it works!

# Options -- Downgrader
**Get package by upgrade** Sort packages to downgrade by the last time a package was upgraded with pacman, be it with `pacman -Syu` or `pacman -S`.

**Get package by time** Sort packages by time between upgrades. This means that is two packages were updated with separate commands but with a set amount of time of each other, both can still be downgraded.

**Print all packages** Simply prints information about found packages. Prints name, date upgraded, old version name, and new version name.

**Downgrade only specific packages** Allows you to select which packages to downgrade and which ones to keep the same. Simply enter numbers or a range of numbers corresponding to which packages to downgrade.

**Print Command** Prints a command which you can run to downgrade all selected packages, or all packages if you didn't select any

**Downgrade** Runs the pacman command to downgrade all selected packages.

# Options -- Package Selecter - Package Selection
**_spacebar_** Selects the currently highlighted package to be worked on

**_left_arrow_** Shifts to previous initial key.

**_right_arrow_** Shifts to next initial key.

**_down_arrow_** Shifts to next package in list.

**_up_arrow_** Shifts to previous package in list.

**j** Jump to a specific key. Enter the letter or number corresponding to the key to jump to it

**s** Select or deselect a range of packages. Enter the first index of the range, then the last index. The range is inclusive.

**e** Acknowledge selected list. Exits out of the screen and brings you to version selection :)

# Options -- Package Selecter - Version Selection
**_spacebar_** Selects the currently highlighted version to be used

**_left_arrow_** Shifts to previous package.

**_right_arrow_** Shifts to next package.

**_down_arrow_** Shifts to next version in list.

**_up_arrow_** Shifts to previous versoin in list.

**e** Acknowledge selected versions. Packages without a selected version will not be modified. Exits out of the screen and downgrades the packages for you. `--noconfirm` is not used, so this gives you the chance to review what changes you'll be making.
