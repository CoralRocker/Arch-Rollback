import pacman
import curses

def main(stdscr):
    
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)
    stdscr.keypad(True)
    stdscr.clear()
    height, width = stdscr.getmaxyx()
    stdscr.addstr(int(height/2), int(width/2 - 20), "Initializing Package List. Please Wait")
    stdscr.refresh()
    l = pacman.pacman_list()
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
    while True:
        stdscr.clear()
        key = list(l.alphabetised.keys())[current_key]
        string = f"KEY: {key.upper()}"
        stdscr.addstr(0, int(width/2 - len(string)), string, curses.A_STANDOUT | curses.A_BOLD)
        pkg_list = l.alphabetised[key]
        num_items = len(pkg_list)
        offset = 0
        space_len = len(str(len(pkg_list)))
        for index, pkg in enumerate(pkg_list, 1):
            if index+offset == height:
                break
            if index + 1 > offset:
                stdscr.addstr(index + offset, 0, "("+(" "*(space_len-len(str(index))))+str(index)+") ", curses.color_pair(1)) # Gets correctly formatted index
                stdscr.addstr(str(pkg), (curses.A_REVERSE if current_item == index-1 else 0)|(curses.A_REVERSE if index-1 in multiselect_indeces[key] else 0))
        
        c = stdscr.getch()
        if chr(c).lower() == 'q':
            break
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
            if current_item - offset == height:
                offset += 1
        elif c == curses.KEY_UP:
            current_item = (current_item - 1 if current_item - 1 >= 0 else 0)
        elif chr(c) == ' ':
            if current_item in multiselect_indeces[key]:
                multiselect_indeces[key].remove(current_item)
            else:
                multiselect_indeces[key].append(current_item)
        stdscr.refresh()


curses.wrapper(main)
