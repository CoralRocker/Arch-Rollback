import pacman
import cache

pacList = pacman.pacman_list()
print("Sorting Packages")
pacList.sortCachePackages()
print("Sorted packages")
pacList.getWebCachedPackages(debug=True)
print("Cached Packages")
myCache = cache.cache(debug=True)
myCache.updateCache(pacList.alphabetised)
myCache.savePackages()
