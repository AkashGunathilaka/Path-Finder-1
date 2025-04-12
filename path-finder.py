import curses
from curses import wrapper
import time
import queue
from mazes import mazes


# This program is a simple pathfinding visualizer using the BFS algorithm.


def print_maze(maze_choice, stdscr, path=[]):
    GREEN = curses.color_pair(1)
    RED = curses.color_pair(2)


    for i, row in enumerate(maze_choice):
        for j, value in enumerate(row):
            if (i, j) in path:
                stdscr.addstr(i , j * 2, 'X', RED)
            else:
                stdscr.addstr(i , j * 2, value, GREEN)


def find_start(maze_choice, start):

    for i, row in enumerate(maze_choice):
        for j, value in enumerate(row):
            if value == start:
                return i, j

    return None


def find_path(maze_choice, stdscr):
    start ="O"
    end ="X"
    start_pos = find_start(maze_choice, start)

    q = queue.Queue()


    q.put((start_pos, [start_pos]))

    visited = set() # keep track of the visited nodes

    while not q.empty():
        current_pos, path = q.get()
        # we are getting the current position and the path from the queue this is unpacking the tuple that we put in the queue
        row, col = current_pos # we are unpacking the current position into row and column

        stdscr.clear()
        print_maze(maze_choice, stdscr, path)
        time.sleep(0.1)
        stdscr.refresh()

        if maze_choice[row][col] == end:
            return path

        neighbors = find_neighbors(maze_choice, row, col)
        for neighbor in neighbors:
            if neighbor in visited:
                continue

            r, c = neighbor
            if maze_choice[r][c] == "#":
                continue

            new_path = path +[neighbor]
            q.put((neighbor, new_path))
            visited.add(neighbor)

def find_neighbors(maze_choice, row, col):
    neighbors = []

    if row > 0:
        neighbors.append((row - 1, col))
    if row + 1 < len(maze_choice):
        neighbors.append((row + 1, col))

    if col > 0:
        neighbors.append((row, col - 1))

    if col + 1 < len(maze_choice[0]):
        neighbors.append((row, col + 1))
    return neighbors


def main(stdscr):
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_BLACK)

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "Available Mazes:")
        stdscr.addstr(1, 0, "1 - Maze 1")
        stdscr.addstr(2, 0, "2 - Maze 2")
        stdscr.addstr(3, 0, "3 - Maze 3")
        stdscr.addstr(5, 0, "Select a maze (1/2/3) or press 'q' to quit: ")
        stdscr.refresh()

        maze_choice = None

        while True:
            choice = stdscr.getch()

            if choice == ord('1'):
                maze_choice = mazes["Maze 1"]
                break
            elif choice == ord('2'):
                maze_choice = mazes["Maze 2"]
                break
            elif choice == ord('3'):
                maze_choice = mazes["Maze 3"]
                break
            elif choice == ord('q') or choice == ord('Q'):
                return  # Exit the program
            else:
                stdscr.addstr(7, 0, "Invalid choice. Please select 1, 2, or 3.")
                stdscr.refresh()
                time.sleep(1)
                stdscr.clear()
                stdscr.addstr(0, 0, "Available Mazes:")
                stdscr.addstr(1, 0, "1 - Maze 1")
                stdscr.addstr(2, 0, "2 - Maze 2")
                stdscr.addstr(3, 0, "3 - Maze 3")
                stdscr.addstr(5, 0, "Select a maze (1/2/3) or press 'q' to quit: ")

        stdscr.clear()
        print_maze(maze_choice, stdscr)
        find_path(maze_choice, stdscr)


        stdscr.addstr(len(maze_choice) + 2, 0, "Pathfinding complete! Press any key to return to the menu...")
        stdscr.refresh()
        stdscr.getch()

wrapper(main)
