# make_maze original code https://rosettacode.org/wiki/Maze_generation#Python

import csv
import argparse
from random import shuffle, randrange, randint


def generate_entry_exit(hor):
    h = len(hor)

    entry_pos = randint(0, len(hor[0]) - 2)
    exit_pos = randint(0, len(hor[h - 1]) - 2)

    hor[0][entry_pos] = "+  "
    hor[h - 1][exit_pos] = "+  "

    return hor


def generate_csv(s):
    with open('maze.csv', 'w', newline='') as csvfile:
        maze_writer = csv.writer(csvfile, dialect='excel')

        for str in s.split('\n'):
            if (len(str) == 0):
                continue
            maze_writer.writerow([ch for ch in str])


def display_csv():
    try:
        with open('maze.csv', newline='') as csvfile:
            maze_reader = csv.reader(csvfile, delimiter=',')
            for row in maze_reader:
                print(''.join(row))
    except FileNotFoundError:
        print("maze.csv not found")


def make_maze(w, h):
    vis = [[0] * w + [1] for _ in range(h)] + [[1] * (w + 1)]
    ver = [["|  "] * w + ['|'] for _ in range(h)] + [[]]
    hor = [["+--"] * w + ['+'] for _ in range(h + 1)]

    def walk(x, y):
        vis[y][x] = 1

        d = [(x - 1, y), (x, y + 1), (x + 1, y), (x, y - 1)]
        shuffle(d)
        for (xx, yy) in d:
            if vis[yy][xx]:
                continue
            if xx == x:
                hor[max(y, yy)][x] = "+  "
            if yy == y:
                ver[y][max(x, xx)] = "   "
            walk(xx, yy)

    walk(randrange(w), randrange(h))

    hor = generate_entry_exit(hor)

    s = ""
    for (a, b) in zip(hor, ver):
        s += ''.join(a + ['\n'] + b + ['\n'])

    generate_csv(s)
    display_csv()

    print("A %sx%s maze generated and written to maze.cvs" % (w, h))

    return s


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Generates a maze and write it to maze.csv")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-g", "--generate",
                       nargs=2,
                       metavar=('W', 'H'),
                       help="Generates a new WxH maze and writes it to maze.csv")
    group.add_argument("-d", "--display",
                       help="Display a maze stored in maze.csv",
                       action="store_true")
    args = parser.parse_args()

    if args.generate:
        make_maze(int(args.generate[0]), int(args.generate[1]))
    elif args.display:
        display_csv()
    else:
        parser.print_help()
