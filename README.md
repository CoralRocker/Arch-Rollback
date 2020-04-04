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
|:---:|:---:|---|
| \_\_init__ |  | Sets up the list to be ready to store package information |
| cadd | line | Given _line_ from the pacman log file, will create a new package with the information and add it to the package list
| sort |  | Sorts complete list of packages to contain only packages updated within 30 minutes of each other
| updatePackages|  | Calls on all sorted packages to update their information
| printPackages |  | Prints packages to terminal in a pretty way. Tells when it was last updated and what versions were affected.
| appendSelected | addendum | Adds _addendum_ to list of selected packages. _Addendum_ may be a list or a single package 
| printFiles | numbered=False | Prints packages normally if numbered is false. If numbered is true, prints all packages with numbering before them.
| printCommand | sudo=False | Prints out the command to run to downgrade packages, with sudo if sudo is True
| downgrade |  | Downgrades all selected packages. Essentially runs the output of printCommand. Uses sudo.
| printSelected | selected=False | Prints packages and their previous and new versions if selected is False. If selected is True, prints the packages' selected versions.
| getCachePackages |  | Retrieves a list of all installed packages and creates pacman_package objects for all of them.
| sortCachePackages |  | Sorts the found packages alphabetically in a dictionary by their first initial.
| getWebCachedPackages | debug=False | Gets all available web packages for each installed package. Debug prints some debugging information for each package. ***DON'T USE THIS***
| getSelectWebCachedPackages | alpha_dict | Given a dict sorted by the first initial of packages (alpha_dict), gets web cache for the packages. Does the same thing as getWebCachedPackages, except only for selected packages.

### pacman_package class
| Method Name | Parameters | What It Does |
|:---:|:---:|---|
| \_\_init__ | line=False, regex=False, name=False, ver=False | if given a line and regex, gets the package's update date. If given name and ver, uses it to update the package's name and current version. 
| \_\_str__ |  | prints the package cleanly
| \_\_repr__ |  | Does the same as \_\_str__
| \_\_eq__ |  | Checks for equivalency between packages based on if their names are the same
| date |  | Prints a pretty version of the package's update date and time
| getName | regex | Gets passed a regex and uses it to find the package's name, given that it also has the line passed during its creation
| getVer | regex | Uses the regex to get new version of the package and the old version
| setPkgList | full_list | Gets list of packages in pacman cache. Full_list is the list of files in the pacman cache directory. pacman_list fetches this automatically.
| getWebCache | url | Given the url for an online archive, retrieves all the possible versions of the package online.
| getVersions | flist | Saves all versions of the package found by getWebCache and setPkgList as a tuple containing the version and the url/file path. flist is the full list of installed packages.
| removeWebDuplicates | favor_local=True | Removes duplicate package versions from the cache list, removing web based caches if favor_local is True, or local packages if favor_local is False.
