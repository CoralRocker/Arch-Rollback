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
    offset = 0
    while True:
        stdscr.clear()
        key = list(l.alphabetised.keys())[current_key]
        pkg_list = l.alphabetised[key]
        num_items = len(pkg_list)
        space_len = len(str(len(pkg_list)))
        for index, pkg in enumerate(pkg_list, 1):
            if index < (height + offset) and index >= offset:
                stdscr.addstr(index - offset, 0, "("+(" "*(space_len-len(str(index))))+str(index)+") ", curses.color_pair(1)) # Gets correctly formatted index
                stdscr.addstr(str(pkg), (curses.A_REVERSE if current_item == index-1 else 0)|(curses.A_REVERSE if index-1 in multiselect_indeces[key] else 0))
        string = f"KEY: {key.upper()}"
        stdscr.move(0, 0)
        stdscr.clrtoeol()
        stdscr.addstr(0, int(width/2 - len(string)), string, curses.A_STANDOUT | curses.A_BOLD)
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
            if current_item - offset == height -1 :
                offset += 1
        elif c == curses.KEY_UP:
            current_item = (current_item - 1 if current_item - 1 >= 0 else 0)
            if current_item - offset < 1:
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

        stdscr.refresh()


curses.wrapper(main)
