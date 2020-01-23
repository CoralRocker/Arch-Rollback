import re
import datetime
import time
from os import listdir
from os.path import isfile, join
import configparser

log_file = "/var/log/pacman.log"
cache_dir = "/var/cache/pacman/pkg"
time_difference = 15

config = configparser.ConfigParser()
config.read("downgrader.conf")


log_file = config["DEFAULT"]["LogFile"]
cache_dir = config["DEFAULT"]["CacheDir"]
time_difference = int(config["DEFAULT"]["AllowableDifference"])



'''
Wrapper class for pacman_package class. 
Allows for a list of upgraded packages,
then for downgrading said packages.
'''
class pacman_list:
    '''
    NameRegex is to retrieve name of programs
    VerRegex is to retrieve version of programs
    cache_dir_list is list of all cached pacman packages
    '''
    def __init__(self):
        self.pkgs = []
        self.NameRegex = re.compile("(?<=(upgraded ))[a-zA-z\d\-\_\.]+?(?= \()")
        self.VerRegex = re.compile("(?<=\()([\_a-zA-Z\d\.\-\+\:]+) -> ([\_a-zA-Z\d\.\-\+\:]+)(?=\))")   
        self.cache_dir_list = [f for f in listdir(cache_dir) if isfile(join(cache_dir, f))]
        self.regex = re.compile("(?<=(\[)).*?(?=-\d\d\d\d\])")
        self.selected_packages = []
        self.sorted = False

    # Add to list
    def add(self, package):
        self.pkgs.append(package)
    
    # Add to list without needing to already have a package created
    def cadd(self, line):
        pkg = pacman_package(line, self.regex)
        self.pkgs.append(pkg)

    # Repopulate list with packages updated within 30 minute of each other.
    def sort(self):
        pkg_date = self.pkgs[len(self.pkgs)-1]._date #datetime.datetime(1970, 1, 1, 0, 0, 0)
        good_list = []
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

    # Call on sorted packages to update their own information
    def updatePackages(self):
        for pkg in self.pkgs:
            pkg.getName(self.NameRegex)
            pkg.getVer(self.VerRegex)
            pkg.setPkgList(self.cache_dir_list)
            pkg.getPackageFiles()

    # Prints some debugging information about packages
    def printPackages(self):
        for pkg in self.pkgs:
            print(f"{pkg.pkg_name} upgraded on {pkg._date} from {pkg.old_ver} to {pkg.new_ver}")
    
    def printFiles(self, numbered=False):
        if not numbered:
            for pkg in self.pkgs:
                print(f"{pkg.pkg_name} {pkg.pkg_files}")
        else:
            space_len = len(str(len(self.pkgs)))
            for index, pkg in enumerate(self.pkgs):
                out = "("+(" "*(space_len-len(str(index))))+str(index+1)+") " # Gets correctly formatted index
                out += pkg.pkg_name + " " + str(pkg.old_ver) + " -> " + str(pkg.new_ver) # Adds package name and versions
                print(out)

    def downgrade(self):
        command = ["pacman", "-U"]
        for pkg in self.pkgs:
            command.append(pkg.pkg_files[1])
        process = subprocess.Popen(command, stdin=subprocess.PIPE, stderr=subprocess.PIPE, stdout=subprocess.PIPE, universal_newlines=True)
        while True:
            output = process.stdout.readline()
            print(output.strip())
            # Do something else
            return_code = process.poll()
            '''
            if return_code is not None:
                print('RETURN CODE', return_code)
                # Process has finished, read rest of the output 
                for output in process.stdout.readlines():
                    print(output.strip())
                break
            '''
    
   # def getCommand(self):

    # Prints out full command to run, perhaps with sudo
    def printCommand(self, sudo=False):
        command = ("sudo " if sudo else "") + "pacman -U"
        for pkg in self.pkgs:
            command += " " + pkg.pkg_files[1]
        print(command)

    def getPackages(self, inputString):
        # 1-2 3 556
        if not self.sorted:
            self.sort()
            self.sorted = True
        pkg = list(filter(None, re.split(',| ', inputString)))
        regex = re.compile("(\d+)-(\d+)")
        indeces = []
        for num in pkg:
            if re.search("-", num):
                nums = [int(regex.search(num).group(1)), int(regex.search(num).group(2))]
                for i in range(nums[0], nums[1]+1):
                    indeces.append(i)
            else:
                indeces.append(int(num))
        indeces = list(dict.fromkeys(indeces))
        self.selected_packages = [self.pkgs[i-1] for i in indeces]

    def printSelected(self):
        for pkg in self.selected_packages:
            print(f"{pkg.pkg_name} {pkg.old_ver} -> {pkg.new_ver}")

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
    def __init__(self, line, regex):
        self.line = line
        tmp = regex.search(line).group(0)
        self._date = datetime.datetime.strptime(tmp, "%Y-%m-%dT%X")
    
    # Returns a pretty version of the date
    def date(self):
        return self._date.strftime("%c")

    # Gets passed a regex from the wrapper class (pacman_list), uses it to get name
    def getName(self, regex):
        self.pkg_name = regex.search(self.line).group(0)
    
    # Gets passed a regex from the wrapper class, uses it to get old and new version
    def getVer(self, regex):
        self.old_ver = regex.search(self.line).group(1)
        self.new_ver = regex.search(self.line).group(2)

    # Get list of cached packages for program
    def setPkgList(self, full_list):
        regexp = "^"+self.pkg_name+"-"
        self.pkglist = [f for f in full_list if re.search(regexp, f)]

    def getPackageFiles(self):
        self.pkg_files = ["", ""]
        regexp_new = "^"+self.pkg_name+"-"+self.new_ver
        regexp_old = "^"+self.pkg_name+"-"+self.old_ver
        for f in self.pkglist:
            if re.search(regexp_new, f):
                self.pkg_files[1] = cache_dir+('/' if cache_dir[len(cache_dir)-1] != '/' else '')+f
            elif re.search(regexp_old, f):
                self.pkg_files[0] = cache_dir+('/' if cache_dir[len(cache_dir)-1] != '/' else '')+f

