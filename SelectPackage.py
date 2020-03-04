import pacman
import curses
import re
from cache import cache

selected_packages = dict()
l = pacman.pacman_list()
exit = False

def main(stdscr):
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)
    stdscr.keypad(True)
    stdscr.clear()
    height, width = stdscr.getmaxyx()
    stdscr.addstr(int(height/2), int(width/2 - 20), "Initializing Package List. Please Wait")
    stdscr.refresh()
    l.getCachePackages()
    l.sortCachePackages() 
    
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_RED, -1)
    curses.init_pair(2, curses.COLOR_GREEN, -1)

    current_key = 0
    max_key = len(l.alphabetised.keys())
    current_item = 0
    multiselect_indeces = dict()
    for k in l.alphabetised.keys():
        multiselect_indeces[k] = []
    offset = 0
    instr_h = 8

    while True:
        stdscr.erase()
        
        # Print Package List
        key = list(l.alphabetised.keys())[current_key]
        pkg_list = l.alphabetised[key]
        num_items = len(pkg_list)
        space_len = len(str(len(pkg_list)))
        for index, pkg in enumerate(pkg_list, 1):
            if index < (height + offset - instr_h) and index >= offset:
                stdscr.addstr(index - offset, 0, "("+(" "*(space_len-len(str(index))))+str(index)+") ", curses.color_pair(2 if index -1 in multiselect_indeces[key] else 1)) # Gets correctly formatted index
                stdscr.addstr(str(pkg), (curses.A_REVERSE if current_item == index-1 else 0)|(curses.A_REVERSE if index-1 in multiselect_indeces[key] else 0))
        
        # Print Key Title Screen
        string = f"KEY: {key.upper()}"
        stdscr.move(0, 0)
        #stdscr.clrtoeol()
        stdscr.addstr(0, int(width/2 - len(string)/2), string, curses.A_STANDOUT | curses.A_BOLD)
        
        # Print Instructions
        for x in range(0, width):
            for y in range(0, height):
                if y == height - instr_h:
                    if x == 0:
                        stdscr.insch(y, x, curses.ACS_ULCORNER)
                    elif x == width - 1:
                        stdscr.insch(y, x, curses.ACS_URCORNER)
                    else:
                        stdscr.insch(y, x, curses.ACS_HLINE)
                elif y == height - 1:
                    if x == 0:
                        stdscr.insch(y, x, curses.ACS_LLCORNER)
                    elif x == width - 1:
                        stdscr.insch(y, x, curses.ACS_LRCORNER)
                    else:
                        stdscr.insch(y, x, curses.ACS_HLINE)
                elif y > height - instr_h:
                    if x == 0:
                        stdscr.insch(y, x, curses.ACS_VLINE)
                    elif x == width - 1:
                        stdscr.insch(y, x, curses.ACS_VLINE)
        
        stdscr.insstr(height - instr_h + 1, int(width / 2 - 5), 'HOW-TO-USE', curses.A_STANDOUT)
        stdscr.insstr(height - instr_h + 6, 1, 'Press J to jump to a specific index')
        stdscr.insstr(height - instr_h + 5, 1, 'Press S to select multiple packages')
        stdscr.insstr(height - instr_h + 4, 1, 'Press Q to exit program')
        stdscr.insstr(height - instr_h + 3, 1, 'Press E to confirm selections and exit program')
        stdscr.insstr(height - instr_h + 2, 1, 'Press space to select a package')

        c = stdscr.getch()
        if chr(c).lower() == 'q':
            curses.echo()
            curses.nocbreak()
            curses.curs_set(1)
            stdscr.move(height-1, 0)
            stdscr.clrtoeol()
            stdscr.addstr(height-1, 0, "Press Y to confirm Exit. You WILL LOSE ALL SELECTIONS: ")
            stdscr.refresh()
            c = chr(stdscr.getch()).lower()
            curses.noecho()
            curses.cbreak()
            curses.curs_set(0)
            if c == 'y':
                curses.endwin()
                quit()
        elif c == curses.KEY_RIGHT:
            current_key = (current_key + 1 if current_key + 1 < max_key else 0)
            current_item = 0
            offset = 0
        elif c == curses.KEY_LEFT:
            current_key = (current_key - 1 if current_key - 1 >= 0 else max_key - 1)
            current_item = 0
            offset = 0
        elif c == curses.KEY_DOWN:
            current_item = (current_item + 1 if current_item + 1 < num_items else num_items - 1)
            if current_item - offset == height - 1 - instr_h :
                offset += 1
        elif c == curses.KEY_UP:
            current_item = (current_item - 1 if current_item - 1 >= 0 else 0)
            if current_item - offset < 0:
                offset -= 1
        elif chr(c) == ' ':
            if current_item in multiselect_indeces[key]:
                multiselect_indeces[key].remove(current_item)
            else:
                multiselect_indeces[key].append(current_item)
        elif chr(c) == 'j':
            # Jump to specific key
            curses.echo()
            curses.nocbreak()
            curses.curs_set(1)
            while 1:
                stdscr.move(height-1, 0)
                stdscr.clrtoeol()
                stdscr.addstr(height-1, 0, "Enter key to access: ")
                stdscr.refresh()
                c = chr(stdscr.getch())
                if c in l.alphabetised.keys():
                    current_key = list(l.alphabetised.keys()).index(c)
                    break
                else:
                    tmp = f"{c} is not a valid key"
                    stdscr.move(height-2, 0)
                    stdscr.clrtoeol()
                    stdscr.addstr(height-2, 0, tmp)
    
            curses.noecho()
            curses.cbreak()
            curses.curs_set(0)
        elif chr(c) == 's':
            curses.echo()
            curses.nocbreak()
            curses.curs_set(1)
            nums = []
            ranged = False
            while 1:
                stdscr.move(height-1, 0)
                stdscr.clrtoeol()
                stdscr.addstr(height-1, 0, "Enter first number Or a Range: ")
                stdscr.refresh()
                c = stdscr.getstr()
                t = 0
                try:
                     t = int(c)
                except:
                    
                    regex = re.compile("(\d+)\ *-\ *(\d+)")
                    if not regex.search(str(c)):
                        tmp = f"{str(c)} is not a valid number"
                        stdscr.move(height-2, 0)
                        stdscr.clrtoeol()
                        stdscr.addstr(height-2, 0, tmp)
                    else:
                        ranged = True
                        nums.append(int(regex.search(str(c)).group(1)))
                        nums.append(int(regex.search(str(c)).group(2)))
                        nums.sort()
                        break
                if t and not ranged:
                    nums.append(t)
                    break
            if not ranged:
                while 1:
                    stdscr.move(height-1, 0)
                    stdscr.clrtoeol()
                    stdscr.addstr(height-1, 0, "Enter second number: ")
                    stdscr.refresh()
                    c = stdscr.getstr()
                    t = 0
                    try:
                         t = int(c)
                    except:
                        tmp = f"{str(c)} is not a valid number"
                        stdscr.move(height-2, 0)
                        stdscr.clrtoeol()
                        stdscr.addstr(height-2, 0, tmp)
                    if t:
                        nums.append(t)
                        break
            nums.sort()
            for num in range(nums[0], nums[1]+1):
                if num-1 > -1 and num-1 < len(pkg_list):
                    if num-1 in multiselect_indeces[key]:
                        multiselect_indeces[key].remove(num-1)
                    else:
                        multiselect_indeces[key].append(num-1)


            curses.noecho()
            curses.cbreak()
            curses.curs_set(0)
        elif chr(c) == 'e':
            curses.echo()
            curses.nocbreak()
            curses.curs_set(1)
            stdscr.move(height-1, 0)
            stdscr.clrtoeol()
            stdscr.addstr(height-1, 0, "Press Y to confirm Exit: ")
            stdscr.refresh()
            c = chr(stdscr.getch()).lower()
            curses.noecho()
            curses.cbreak()
            curses.curs_set(0)
            if c == 'y':
                for key in list(l.alphabetised.keys()):
                    selected_packages[key] = []
                    for index in multiselect_indeces[key]:
                        selected_packages[key].append(l.alphabetised[key][index])
                break            
        stdscr.refresh()

def SelectPackageVersions(stdscr):
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)
    stdscr.keypad(True)
    stdscr.clear()
    height, width = stdscr.getmaxyx()
    
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_RED, -1)
    curses.init_pair(2, curses.COLOR_GREEN, -1)
    count = 0
    for k in selected_packages.keys():
        for i in selected_packages[k]:
            count += 1
    
    paccache = cache()
    if paccache.exists == False:
        tmp = f"Retrieving {count} packages. This may take up to {count * 5} seconds"
        stdscr.addstr(int(height/2), int(width/2 - len(tmp)/2), tmp)
        stdscr.refresh()
        l.getSelectWebCachedPackages(selected_packages)
        paccache.updateCache(l.selected_packages)
    else:
        pc_l = []
        pc_d = dict()
        for k in selected_packages.keys():
            for f in selected_packages[k]:
                pc_l.append(f)
        ret = paccache.getSelectedPackages(pc_l)
        count = 0
        if len(ret) != len(pc_l):
            for pkg in pc_l:
                if pkg not in ret:
                    if pkg.pkg_name[0] not in pc_d.keys():
                        pc_d[pkg.pkg_name[0]] = []
                        pc_d[pkg.pkg_name[0]].append(pkg)
                        count += 1
            tmp = f"Supplementing {count} packages. This may take up to {count * 5} seconds"
            stdscr.addstr(int(height/2), int(width/2 - len(tmp)/2), tmp)
            stdscr.refresh()
            l.getSelectWebCachedPackages(pc_d)
        l.appendSelected(ret)
        # tmp = f"Retrieved {len(ret)} packages"
        # stdscr.addstr(int(height/2), int(width/2 - len(tmp)/2), tmp)
        # stdscr.refresh()
        # import time
        # time.sleep(2)
        paccache.updateCache(l.selected_packages) 
    
    paccache.savePackages()

    current_pkg = 0
    max_pkg = len(l.selected_packages)
    selected_version = dict()
    selected_index = dict()
    for pkg in l.selected_packages:
        pkg.full_cache.sort(key=lambda x: x[0])
        selected_version[pkg.pkg_name] = None
        selected_index[pkg.pkg_name] = -1

    current_item = 0
    offset = 0
    instr_h = 6

    while True:
        stdscr.clear()
        cur_item = l.selected_packages[current_pkg]
        num_items = len(cur_item.full_cache)
        space_len = len(str(len(cur_item.full_cache)))

        for index, pkg in enumerate(cur_item.full_cache , 1):
            if index < (height + offset - instr_h) and index >= offset:
                stdscr.addstr(index - offset, 0, "("+(" "*(space_len-len(str(index))))+str(index)+") ", curses.color_pair(2 if index-1 == selected_index[cur_item.pkg_name]  else 1)) # Gets correctly formatted index
                stdscr.addstr(str(pkg), (curses.A_REVERSE if current_item == index-1 else 0))
                if pkg[0] == cur_item.new_ver:
                    stdscr.addstr(" CURRENTLY INSTALLED", curses.color_pair(2))
        string = f"KEY: {cur_item.pkg_name} Selected Version: {cur_item.full_cache[selected_index[cur_item.pkg_name]][0] if selected_index[cur_item.pkg_name] != -1 else 'None'}"
        stdscr.move(0, 0)
        stdscr.clrtoeol()
        stdscr.addstr(0, int(width/2 - len(string)/2), string, curses.A_STANDOUT | curses.A_BOLD)
        
        # Print Instructions
        for x in range(0, width):
            for y in range(0, height):
                if y == height - instr_h:
                    if x == 0:
                        stdscr.insch(y, x, curses.ACS_ULCORNER)
                    elif x == width - 1:
                        stdscr.insch(y, x, curses.ACS_URCORNER)
                    else:
                        stdscr.insch(y, x, curses.ACS_HLINE)
                elif y == height - 1:
                    if x == 0:
                        stdscr.insch(y, x, curses.ACS_LLCORNER)
                    elif x == width - 1:
                        stdscr.insch(y, x, curses.ACS_LRCORNER)
                    else:
                        stdscr.insch(y, x, curses.ACS_HLINE)
                elif y > height - instr_h:
                    if x == 0:
                        stdscr.insch(y, x, curses.ACS_VLINE)
                    elif x == width - 1:
                        stdscr.insch(y, x, curses.ACS_VLINE)
        
        stdscr.insstr(height - instr_h + 1, int(width / 2 - 5), 'HOW-TO-USE', curses.A_STANDOUT)
        stdscr.insstr(height - instr_h + 4, 1, 'Press Q to exit program')
        stdscr.insstr(height - instr_h + 3, 1, 'Press E to confirm selections and exit program')
        stdscr.insstr(height - instr_h + 2, 1, 'Press space to select a package')



        c = stdscr.getch()
        if chr(c).lower() == 'q':
            curses.echo()
            curses.nocbreak()
            curses.curs_set(1)
            stdscr.move(height-1, 0)
            stdscr.clrtoeol()
            stdscr.addstr(height-1, 0, "Press Y to confirm Exit. You WILL LOSE ALL SELECTIONS: ")
            stdscr.refresh()
            c = chr(stdscr.getch()).lower()
            curses.noecho()
            curses.cbreak()
            curses.curs_set(0)
            if c == 'y':
                curses.endwin()
                quit()
        elif c == curses.KEY_RIGHT:
            current_pkg = (current_pkg + 1 if current_pkg + 1 < max_pkg else 0)
            current_item = 0
            offset = 0
        elif c == curses.KEY_LEFT:
            current_pkg = (current_pkg - 1 if current_pkg - 1 >= 0 else max_pkg - 1)
            current_item = 0
            offset = 0
        elif c == curses.KEY_DOWN:
            current_item = (current_item + 1 if current_item + 1 < num_items else num_items - 1)
            if current_item - offset + instr_h == height -1 :
                offset += 1
        elif c == curses.KEY_UP:
            current_item = (current_item - 1 if current_item - 1 >= 0 else 0)
            if current_item - offset < 0:
                offset -= 1
        
        elif chr(c) == ' ':
            if current_item == selected_index[cur_item.pkg_name]:
                selected_index[cur_item.pkg_name] = -1
                selected_version[cur_item.pkg_name] = None
            else:
                selected_index[cur_item.pkg_name] = current_item
                selected_version[cur_item.pkg_name] = cur_item.full_cache[current_item]
        elif chr(c) == 'e':
            curses.echo()
            curses.nocbreak()
            curses.curs_set(1)
            stdscr.move(height-1, 0)
            stdscr.clrtoeol()
            stdscr.addstr(height-1, 0, "Press Y to confirm Exit: ")
            stdscr.refresh()
            c = chr(stdscr.getch()).lower()
            curses.noecho()
            curses.cbreak()
            curses.curs_set(0)
            if c == 'y':
                for pkg in l.selected_packages:
                        pkg.selected_version = selected_version[pkg.pkg_name][1] if selected_version[pkg.pkg_name] != None else None
                        if pkg.selected_version == None:
                            l.selected_packages.remove(pkg)
            break            
        stdscr.refresh()

curses.wrapper(main)
curses.wrapper(SelectPackageVersions)
l.downgrade()
