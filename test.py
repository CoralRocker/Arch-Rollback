import requests
import lzma
import pacnew as pacman

l = pacman.pacman_list()
print("Cache Packages")
l.getCachePackages()
print("\tDone")
print("Sort Packages")
l.sortCachePackages()
print("\tDone")
print("Get Web Index")
l.getWebIndexPackages(l.alphabetised['d'])
print("\tDone")
