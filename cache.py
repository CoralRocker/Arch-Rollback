import pacman
import random
import os.path
import re
import bz2

'''
Allows for quick and simple saving of program data. Usefull for speeding up 
SelectPackage.py.
'''
class cache:
    def __init__(self, filename=False, debug=False):
        self.fname = filename if filename else "_pacman_cache.bin"
        self.exists = False
        self.packages = []
        self.flines = []
        self.loaded = False
        self.logFile = open(".cache.log", "w")
        self.debug = debug
        if os.path.exists(self.fname):
            self.exists = True
            if os.path.getsize(self.fname) != 0:
                self.flines = bz2.decompress(open(self.fname, "rb").read()).decode('utf-8').split('\n')
                print(len(self.flines))
                self.loadPackages()            
        

    def updateCache(self, update):
        if type(update) == list:
            if self.debug:
               self.logFile.write(f"updateCache: Update Size: {len(update)}\n")
            for pkg in update:
                for cur_pkg in self.packages:
                    if cur_pkg.pkg_name == pkg.pkg_name:
                        if self.debug:
                            self.logFile.write(f"  Remove {pkg.pkg_name}\n")
                        self.packages.remove(cur_pkg)
                self.packages.append(pkg)       
        elif type(update) == dict:
            if self.debug:
                self.logFile.write(f"updateCache: Update Size: {len(update)}\n")
            for k in update.keys():
                for pkg in update[k]:
                    for e_pkg in self.packages:
                        if pkg == e_pkg:
                           self.packages.remove(e_pkg)
                    self.packages.append(pkg)

    def getSelectedPackages(self, selected):
        if not self.loaded:
            self.loadPackages()
        outpkg = []
        for pkg in self.packages:
            for s in selected:
                if pkg.pkg_name == s.pkg_name:
                    s.full_cache = pkg.full_cache
                    outpkg.append(s)
        return outpkg

    def loadPackages(self):    
        if not self.exists:
            return None
        self.logFile.write("Load Packages\n")
        lines = self.flines
        num_objects = re.search("(?<=N\_OBJ\:)\d+", lines[0]).group(0)
        curverre =  re.compile("(?<=\{CUR\_VER\s)([\d\w\:\_\-\.]+)(?=\s\})")
        namere =  re.compile("(?<={obj )[\dA-z\-\+\.]+(?= })")
        urlre = re.compile("(?<=\{\{\s)([^\{\}]+) , ([^\}\{]+)(?=\s\}\})")
        for line in range(1, len(lines)):
            tmp = pacman.pacman_package()
            tmp.pkg_name = namere.search(lines[line]).group(0)
            try:
                tmp.new_ver = curverre.search(lines[line]).group(1)
            except:
                self.logFile.write("Error in regex: "+lines[line]+'\n')
            tmp.full_cache = urlre.findall(lines[line])
            self.packages.append(tmp)
        self.loaded = True
        return self.packages

    def savePackages(self):
        if self.debug:
            self.logFile.write(f"Saving {len(self.packages)} packages\n")
        self.flines = []
        self.flines.append(f"N_OBJ:{len(self.packages)}")
        for obj, pkg in enumerate(self.packages):
            tmpo = "{obj "+pkg.pkg_name+" } "
            tmp1 = " {CUR_VER "+pkg.new_ver+" } "
            tmpstr = ""
            if self.debug:
                self.logFile.write(f"   {pkg.pkg_name} cache: {len(pkg.full_cache)}\n")
            for tmp in pkg.full_cache:
                tmpstr += "{{ "+tmp[0]+" , "+tmp[1]+" }} "
            self.flines.append(tmpo + tmp1 + "{URLLIST_"+str(len(pkg.full_cache))+"} "+tmpstr)
        tmpfile = open(self.fname, "wb")
        tmpfile.write(bz2.compress(bytes('\n'.join(self.flines), 'utf-8')))

if __name__ == "__main__":
    pc = cache()
    print(pc.flines)
    for pkg in pc.packages:
        print(f"{pkg.pkg_name} {pkg.full_cache}")
