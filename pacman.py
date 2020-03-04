import re
import datetime
import time
from os import listdir
from os.path import isfile, join
from colorama import Fore, Back, Style
import subprocess
import string
import requests

prev_cache_file = False

log_file = "/var/log/pacman.log"
cache_dir = "/var/cache/pacman/pkg"
time_difference = 15

'''
Wrapper class for pacman_package class. 
Allows for a list of upgraded packages,
then for downgrading said packages.
'''
class pacman_list:
    '''
    This class runs both the UndoUpgrade.py program and the SelectPackage.py program
    and both use different systems, so it's an absolute mess. I'll clean it up after 
    I finish the SelectPackage.py program. Till then, this is awful.
    '''
    def __init__(self):
        '''
        Full list of packages from previous upgrade
        '''
        self.pkgs = []
        
        '''
        Regex used to find name from log
        '''
        self.NameRegex = re.compile("(?<=(upgraded ))[a-zA-z\d\-\_\.]+?(?= \()")
        
        '''
        Regex used to find version from log
        '''
        self.VerRegex = re.compile("(?<=\()([\_a-zA-Z\d\.\-\+\:]+) -> ([\_a-zA-Z\d\.\-\+\:]+)(?=\))")   
        
        '''
        Full list of packages in cache directory
        '''
        self.cache_dir_list = [f for f in listdir(cache_dir) if isfile(join(cache_dir, f))]
        
        '''
        Regex used to find date and time of upgrade from log file
        '''
        self.DateRegex = re.compile("(?<=(\[)).*?(?=-\d\d\d\d\])")
        
        '''
        List of packages selected for downgrade
        '''
        self.selected_packages = []
        
        ''' Whether or not the packages have been sorted '''
        self.sorted = False

        ''' Whether or not packages have been selected '''
        self.selected = False
        
        ''' List containing command. '''
        self.cmd = ['sudo pacman -U']        

        self.cached = False

    '''
    Add to list without needing to already have a package created
    '''
    def cadd(self, line):
        pkg = pacman_package(line, self.DateRegex)
        self.pkgs.append(pkg)
    
    '''
    Repopulate list with packages updated within 30 minute of each other.
    '''
    def sort(self):
        pkg_date = self.pkgs[len(self.pkgs)-1]._date #datetime.datetime(1970, 1, 1, 0, 0, 0)
        good_list = []
        # Get all packages withing a certain amount of time from each other
        for pkg in reversed(self.pkgs):
            dif = pkg_date - pkg._date
            dif_min = dif.seconds / 60
            if dif_min < time_difference:
                good_list.append(pkg)
            else:
                break
            pkg_date = pkg._date
        self.pkgs = good_list
        self.sorted = True
    '''
    Call on sorted packages to update their own information
    '''
    def updatePackages(self):
        for pkg in self.pkgs:
            pkg.getName(self.NameRegex) # Sets packages name
            pkg.getVer(self.VerRegex) # Sets package version
            pkg.setPkgList(self.cache_dir_list) # Sets package list for package, given a full list of cached packages
            pkg.getPackageFiles() # Gets necessary files.
            pkg.selected_version = pkg.pkg_files[0]  # Version to downgrade to.
        self.pkgs.sort(key=lambda x: x.pkg_name) # Sort alphabetically.

    '''
    Prints some debugging information about packages
    '''
    def printPackages(self):
        for pkg in self.pkgs:
            print(f"{pkg.pkg_name} upgraded on {Fore.YELLOW}{pkg._date}{Fore.RESET} from {Fore.RED}{pkg.old_ver}{Fore.RESET} to {Fore.GREEN}{pkg.new_ver}{Fore.RESET}")
    
    def appendSelected(self, addendum):
        if type(addendum) == list:
            for p in addendum:
                self.selected_packages.append(p)
        else:
            self.selected_packages.append(addendum)

    '''
    Prints all found packages and their respective files nicely
    '''
    def printFiles(self, numbered=False):
        max_len = 0
        # Find max len of numbers to print
        for pkg in self.pkgs:
            if len(pkg.pkg_name) > max_len:
                max_len = len(pkg.pkg_name)
        max_len += 1

        # Print normally
        if not numbered:
            for pkg in self.pkgs:
                # print(f"{pkg.pkg_name} {pkg.pkg_files}")
                space = ' ' * (max_len - len(pkg.pkg_name))
                print(f"{Fore.CYAN + pkg.pkg_name + Fore.RESET + space}", end='')
                print(f"upgraded on {Fore.YELLOW}{pkg._date}{Fore.RESET} from {Fore.RED}{pkg.old_ver}{Fore.RESET} to {Fore.GREEN}{pkg.new_ver}{Fore.RESET}")
        # Print with numbering beforehand
        else:
            space_len = len(str(len(self.pkgs)))
            for index, pkg in enumerate(self.pkgs):
                out = Fore.GREEN + "("+(" "*(space_len-len(str(index))))+str(index+1)+") " + Fore.RESET # Gets correctly formatted index
                space = ' ' * (max_len - len(pkg.pkg_name))
                out += pkg.pkg_name + space + Fore.RED + str(pkg.old_ver) + Fore.RESET + " -> " + Fore.GREEN + str(pkg.new_ver) + Fore.RESET # Adds package name and versions
                print(out)

    '''
    Prints out full command to run, perhaps with sudo
    '''
    def printCommand(self, sudo=False):
        print(Fore.GREEN + "Copy and paste this into the command line: " + Fore.RESET, end='')
        command = ("sudo " if sudo else "") + "pacman -U"
        for pkg in (self.selected_packages if self.selected else self.pkgs):
            command += " " + pkg.pkg_files[0]
        print(command)

    '''
    Runs the actual downgrade operation. 
    '''
    def downgrade(self):
        for pkg in self.selected_packages:
            self.cmd.append(pkg.selected_version)
        if len(self.cmd) != 0:
            self.cmd = ' '.join(self.cmd)
            subprocess.call(self.cmd, shell=True)

    '''
    Given a string containing the indexes of the selected packages,
    puts the packages in the selected_packages list for future use.
    '''
    def getPackages(self, inputString):
        # 1-2 3 556
        pkg = list(filter(None, re.split(',| ', inputString))) # Split into list of numbers and ranges
        regex = re.compile("(\d+)-(\d+)") # Splits ranges into constituent numbers
        indeces = []
        for num in pkg:
            # If it's a range
            if re.search("-", num):
                nums = [int(regex.search(num).group(1)), int(regex.search(num).group(2))]
                nums.sort()
                # Add all numbers in range inclusive
                for i in range(nums[0], nums[1]+1):
                    indeces.append(i)
            else:
                indeces.append(int(num))
        indeces = list(dict.fromkeys(indeces)) # Remove duplicates
        self.selected_packages = [self.pkgs[i-1] for i in indeces] # Save packages
        self.selected = True

    '''
    Prints all the packages to be updated
    '''
    def printSelected(self, selected=False):
        if not selected:
            for pkg in self.selected_packages:
                print(f"{pkg.pkg_name} {pkg.old_ver} -> {pkg.new_ver}")
        else:
            for pkg in self.selected_packages:
                print(f"{pkg.pkg_name} {pkg.selected_version}")

    '''
    Gets all packages 
    ''' 
    def getCachePackages(self):
        pcmn_installed = list(filter(None, subprocess.run(['/bin/pacman', '-Q'], stdout=subprocess.PIPE).stdout.decode('utf-8').split('\n')))
        self.cache_installed_packages = []
        nameRegex = re.compile("([\d\w\_\-\+]+) ([\_a-zA-Z\d\.\-\+\:]+)")
        for pkg in pcmn_installed:
            m_obj = nameRegex.search(pkg)
            self.cache_installed_packages.append(pacman_package(name=m_obj.group(1), ver=m_obj.group(2)))

        for pkg in self.cache_installed_packages:
            pkg.setPkgList(self.cache_dir_list)
        self.cache_installed_packages = [pkg for pkg in self.cache_installed_packages if len(pkg.pkglist)>0]
        self.cached = True
    
    '''
    Alphabetically Sorts the cached packages into a dict
    '''
    def sortCachePackages(self):
        if not self.cached:
           self.getCachePackages()
        self.cache_installed_packages.sort(key=lambda x: x.pkg_name)
        alpha_packages = dict()
        index = 0
        for pkg in self.cache_installed_packages:
            try:
                alpha_packages[pkg.pkg_name[0].lower()].append(pkg)
            except KeyError:
                alpha_packages[pkg.pkg_name[0].lower()] = []
                alpha_packages[pkg.pkg_name[0].lower()].append(pkg)
        self.alphabetised = alpha_packages
    
    '''
    As great as this method is, don't use it.
    Only cache specific packages one at a time for efficiency's sake.
    '''
    def getWebCachedPackages(self, debug=False):
        rxp = re.compile("(?<=href=\")([\w\d\-\_]+)(?=\/)")
        for key in self.alphabetised.keys():
            if debug:
                print("Getting key "+key)
            url = 'https://archive.archlinux.org/packages/'+key+'/'
            index_list = requests.get(url).content.decode('utf-8').split('\r\n')
            web_packages = [rxp.search(pkg).group(1) for pkg in index_list if rxp.search(pkg)]
            for pkg in self.alphabetised[key]:
                if pkg.pkg_name in web_packages:
                    if debug:
                        print("\tGetting "+pkg.pkg_name)
                    pkg.getWebCache(url+pkg.pkg_name+'/')

    '''
    Basically the same as getWebCachedPackages, but much more efficient because it only
    retrieves the selected packages. Also puts the selected packages in self.selected_packages
    for downgrading and ease of access
    '''
    def getSelectWebCachedPackages(self, alpha_dict):
        rxp = re.compile("(?<=href=\")([\w\d\-\_]+)(?=\/)")
        for key in alpha_dict.keys():
            if len(alpha_dict[key]) < 1:
                continue
            url = 'https://archive.archlinux.org/packages/'+key+'/'
            index_list = requests.get(url).content.decode('utf-8').split('\r\n')
            web_packages = [rxp.search(pkg).group(1) for pkg in index_list if rxp.search(pkg)]
            for pkg in alpha_dict[key]:
                if pkg.pkg_name in web_packages:
                    pkg.getWebCache(url+pkg.pkg_name+'/')
        self.selected_packages = []
        for k in alpha_dict.keys():
            for item in alpha_dict[k]:
                self.selected_packages.append(item)
                item.key = k
        self.selected = True
        for pkg in self.selected_packages:
            pkg.setPkgList(self.cache_dir_list)
            pkg.getVersions(self.alphabetised)
            pkg.removeWebDuplicates()    
            


'''
Class holding package information
Allows for easy sorting and retrieving of packages for downgrading

'''
class pacman_package:
    
    '''
    Initialize. 
    "regex" is a global regex object which retrieves the date
    _date is important for sorting objects
    '''
    def __init__(self, line=False, regex=False, name=False, ver=False):
        if line and regex:
            self.line = line
            tmp = regex.search(line).group(0)
            self._date = datetime.datetime.strptime(tmp, "%Y-%m-%dT%X")
        if name and ver:
            self.pkg_name = name
            self.new_ver = ver
            self.old_ver = '0'
            self.key = None
        else:
            self.new_ver = '0'
            self.old_ver = '0'
        self.select_version = None
        self.full_cache = []

    '''
    Print packages cleanly
    '''
    def __str__(self):
        return f"{self.pkg_name} {self.old_ver} {self.new_ver}"
    
    '''
    Same as __str__ but for lists and stuff
    '''
    def __repr__(self):
        return self.__str__()
   
    def __eq__(self, other):
        return self.pkg_name == other.pkg_name

    '''
    Returns a pretty version of the date
    '''
    def date(self):
        return self._date.strftime("%c")

    '''
    Gets passed a regex from the wrapper class (pacman_list), uses it to get name
    '''
    def getName(self, regex):
        self.pkg_name = regex.search(self.line).group(0)    
    
    '''
    Gets passed a regex from the wrapper class, uses it to get old and new version
    '''
    def getVer(self, regex):
        self.old_ver = regex.search(self.line).group(1)
        self.new_ver = regex.search(self.line).group(2)

    '''
    Get list of cached packages for program
    '''
    def setPkgList(self, full_list):
        regexp = "^"+re.escape(self.pkg_name)+"-"
        self.pkglist = [f for f in full_list if re.search(regexp, f)]
    
    '''
    Using Cache Directory, get full names of both current and previous file
    '''
    def getPackageFiles(self):
        self.pkg_files = ["", ""]
        regexp_new = "^"+self.pkg_name+"-"+self.new_ver
        regexp_old = "^"+self.pkg_name+"-"+self.old_ver
        for f in self.pkglist:
            if re.search(regexp_new, f):
                self.pkg_files[1] = cache_dir+('/' if cache_dir[len(cache_dir)-1] != '/' else '')+f
            elif re.search(regexp_old, f):
                self.pkg_files[0] = cache_dir+('/' if cache_dir[len(cache_dir)-1] != '/' else '')+f
    
    '''
    Given the url for the package archive, finds all possible versions of the package
    and saves its url for later useage.
    '''
    def getWebCache(self, url):
        index = requests.get(url).content.decode('utf-8').split('\r\n')
        ename = re.escape(self.pkg_name)
        index = [f for f in index if re.search(ename, f)]
        index = [f for f in index if re.search("href=\""+ename, f)]
        rxp = re.compile("(?<=href=\")(.+)(?=\">)")
        index = [rxp.search(f).group(1) for f in index if rxp.search(f)]
        index = list(set(index))
        index = [ f for f in index if not re.search("\.sig$", f) ] 
        self.web_cached = True
        urls = [url+f for f in index]
        rxp = re.compile(ename+'-(.+)(?=(-|-x86_64|-any).pkg.tar.)')
        names = [rxp.search(f).group(1) for f in index if rxp.search(f)]
        self.full_cache = []
        for i in range(0, len(names)):
            self.full_cache.append((names[i], urls[i]))
        # print(f"Retrieved {self.pkg_name}")
       

    '''
    Because some packages may have both web caching and local caching, this method retrieves all 
    locally cached package versions. 
    Previously, there was a bug where packages such as 'bluez' which have helper packages such as 
    'bluez-utils' or 'bluez-lib' would have it and all helper packages retrieved together. It has 
    been fixed. 
    '''
    def getVersions(self, flist):
        close = []
        for pkg in flist[self.key]:
            if re.search(re.escape(self.pkg_name), pkg.pkg_name):
                close.append(pkg.pkg_name)
        rxp = re.compile('^'+re.escape(self.pkg_name)+'-(.+)(?=(-|-x86_64|-any)\.pkg)')
        brxp = [re.compile('^('+re.escape(pkg)+')-(.+)(?=\.pkg)') for pkg in close if pkg != self.pkg_name]
        
        for pkg in self.pkglist:
            bad = False
            for rx in brxp:
                if rx.search(pkg):
                    # print(f"Bad {rx.search(pkg).group(1)} for good {self.pkg_name}")
                    bad = True
            if rxp.search(pkg) and not bad:
                self.full_cache.append((rxp.search(pkg).group(1), cache_dir+'/'+pkg))
                # print(f"{self.pkg_name} :: {rxp.search(pkg).group(1)}")
        self.full_cache.sort(key=lambda x: x[0])


    '''
    Removes duplicates in web cached items, by default favoring locally cached packages. 
    If the favor_local argument is False, will favor web packages.
    '''
    def removeWebDuplicates(self, favor_local=True):
        for tpl in self.full_cache:
            dup_indexes = [i for i,v in enumerate(self.full_cache) if v[0] == tpl[0]]
            if len(dup_indexes) > 1:
                # Get indexes of duplicate versions with different cache methods.
                # There should never be more than one alternative.
                url_indexes = [i for i in dup_indexes if re.search("https://", self.full_cache[i][1])]
                local_indexes = [i for i in dup_indexes if re.search(re.escape(cache_dir), self.full_cache[i][1])]
                
                url_indexes.sort()
                local_indexes.sort()

                if favor_local:
                    # Reversed so that removals do not affect each other.
                    #for i in reversed(url_indexes):
                    self.full_cache.pop(url_indexes[0])
                else:
                    #for i in reversed(local_indexes):
                    self.full_cache.pop(local_indexes[0])

