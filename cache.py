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
    def __init__(self, filename=False):
        self.fname = filename if filename else "pacman_cache.bin"
        self.exists = False
        self.packages = []
        self.flines = []
        self.loaded = False
        if os.path.exists(self.fname):
            self.exists = True
            if os.path.getsize(self.fname) != 0:
                self.flines = bz2.decompress(open(self.fname, "rb").read()).decode('utf-8').split('\n')
                print(len(self.flines))
                self.loadPackages()            
    
    def updateCache(self, update):
        for pkg in update:
            for cur_pkg in self.packages:
                if cur_pkg.pkg_name == pkg.pkg_name:
                    self.packages.remove(cur_pkg)
                self.packages.append(pkg)

    def getSelectedPackages(selected):
        if not self.loaded:
            self.loadPackages()
        outpkg = []
        for pkg in self.packages:
            for s in selected:
                if pkg.pkg_name == s.pkg_name:
                    outpkg.append(pkg)
        return outpkg

    def loadPackages(self):    
        if not self.exists:
            return None
        lines = self.flines
        num_objects = re.search("(?<=N\_OBJ\:)\d+", lines[0]).group(0)
        curverre =  re.compile("(?<=\{CUR\_VER\s)([\d\w\:\_\-\.]+)(?=\s\})")
        namere =  re.compile("(?<={obj )[\dA-z\-\+\.]+(?= })")
        urlre = re.compile("(?<=\{\{\s)([\d\w]+)\s\,\s([\d\w\/\:\.]+)(?=\s\}\})")
        for line in range(1, len(lines)):
            tmp = pacman.pacman_package()
            tmp.pkg_name = namere.search(lines[line]).group(0)
            tmp.pkg_name.cur_ver = curverre.search(lines[line]).group(1)
            tmp.full_cache = urlre.findall(lines[line])
            self.packages.append(tmp)
        self.loaded = True
        return self.packages

    def savePackages(self):
        self.flines = []
        self.flines.append(f"N_OBJ:{len(self.packages)}")
        for obj, pkg in enumerate(self.packages):
            tmpo = "{obj "+pkg.pkg_name+" } "
            tmp1 = " {CUR_VER "+pkg.cur_ver+" } "
            tmpstr = ""
            for tmp in pkg.full_cache:
                tmpstr += "{{ "+tmp[0]+" , "+tmp[1]+" }} "
            self.flines.append(tmpo + tmp1 + "{URLLIST_"+str(len(pkg.full_cache))+"} "+tmpstr)
        tmpfile = open(self.fname, "wb")
        tmpfile.write(bz2.compress(bytes('\n'.join(self.flines), 'utf-8')))

'''
fname = "pacman_cache.bin"

class test:
    def __init__(self):
        self.pkg_name = ""
        self.full_cache = []

pkg_cache = []
for i in range(0, 50):
    tmp = pacman.pacman_package()
    tmp.pkg_name = "pkg"+str(i)
    for x in range(0, random.randint(1,5)):
        tmp.full_cache.append(("ver"+str(x), "/bin/"+str(x)))
    pkg_cache.append(tmp)

mc = cache(fname)
mc.packages = pkg_cache
#mc.loadPackages()
mc.savePackages()
'''
