import pacnew
import curses
import re

selected_packages = dict()
l = pacnew.pacman_list()
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


    while True:
        stdscr.clear()
        key = list(l.alphabetised.keys())[current_key]
        pkg_list = l.alphabetised[key]
        num_items = len(pkg_list)
        space_len = len(str(len(pkg_list)))
        for index, pkg in enumerate(pkg_list, 1):
            if index < (height + offset) and index >= offset:
                stdscr.addstr(index - offset, 0, "("+(" "*(space_len-len(str(index))))+str(index)+") ", curses.color_pair(2 if index -1 in multiselect_indeces[key] else 1)) # Gets correctly formatted index
                stdscr.addstr(str(pkg), (curses.A_REVERSE if current_item == index-1 else 0)|(curses.A_REVERSE if index-1 in multiselect_indeces[key] else 0))
        string = f"KEY: {key.upper()}"
        stdscr.move(0, 0)
        stdscr.clrtoeol()
        stdscr.addstr(0, int(width/2 - len(string)), string, curses.A_STANDOUT | curses.A_BOLD)
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
            if current_item - offset == height -1 :
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
    tmp = f"Retrieving {count} packages. This may take up to {count * 5} seconds"
    stdscr.addstr(int(height/2), int(width/2 - len(tmp)/2), tmp)
    stdscr.refresh()
    l.getSelectWebCachedPackages(selected_packages)
    
    current_pkg = 0
    max_pkg = len(l.selected_packages)
    selected_version = dict()
    selected_index = dict()
    for pkg in l.selected_packages:
        selected_version[pkg.pkg_name] = None
        selected_index[pkg.pkg_name] = -1

    current_item = 0
    offset = 0


    while True:
        stdscr.clear()
        cur_item = l.selected_packages[current_pkg]
        num_items = len(cur_item.full_cache)
        space_len = len(str(len(cur_item.full_cache)))

        for index, pkg in enumerate(cur_item.full_cache , 1):
            if index < (height + offset) and index >= offset:
                stdscr.addstr(index - offset, 0, "("+(" "*(space_len-len(str(index))))+str(index)+") ", curses.color_pair(2 if index-1 == selected_index[cur_item.pkg_name]  else 1)) # Gets correctly formatted index
                stdscr.addstr(str(pkg), (curses.A_REVERSE if current_item == index-1 else 0))
        string = f"KEY: {cur_item.pkg_name} Selected Version: {cur_item.full_cache[selected_index[cur_item.pkg_name]][0] if selected_index[cur_item.pkg_name] != -1 else 'None'}"
        stdscr.move(0, 0)
        stdscr.clrtoeol()
        stdscr.addstr(0, int(width/2 - len(string)), string, curses.A_STANDOUT | curses.A_BOLD)
        c = stdscr.getch()
        if chr(c).lower() == 'q':
            break
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
            if current_item - offset == height -1 :
                offset += 1
        elif c == curses.KEY_UP:
            current_item = (current_item - 1 if current_item - 1 >= 0 else 0)
            if current_item - offset < 1:
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
            break            
        stdscr.refresh()

curses.wrapper(main)
curses.wrapper(SelectPackageVersions)
l.downgrade()
