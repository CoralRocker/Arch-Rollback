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

    current_key = 0
    max_key = len(l.alphabetised.keys())
    current_item = 0
    while True:
        stdscr.clear()
        key = list(l.alphabetised.keys())[current_key]
        string = f"KEY: {key.upper()}"
        stdscr.addstr(0, int(width/2 - len(string)), string, curses.A_STANDOUT | curses.A_BOLD)
        pkg_list = l.alphabetised[key]
        num_items = len(pkg_list)
        offset = 0
        for index, pkg in enumerate(pkg_list, 1):
            if index == height:
                break
            stdscr.addstr(index + offset, 0, str(pkg), (curses.A_REVERSE if current_item == index-1 else 0))
        stdscr.refresh()
        c = stdscr.getch()
        if chr(c).lower() == 'q':
            break
        elif c == curses.KEY_RIGHT:
            current_key = (current_key + 1 if current_key + 1 < max_key else 0)
            current_item = 0
        elif c == curses.KEY_LEFT:
            current_key = (current_key - 1 if current_key - 1 >= 0 else max_key - 1)
            current_item = 0
        elif c == curses.KEY_DOWN:
            current_item = (current_item + 1 if current_item + 1 < num_items else 0)
        elif c == curses.KEY_UP:
            current_item = (current_item - 1 if current_item - 1 >= 0 else num_items - 1)

curses.wrapper(main)
