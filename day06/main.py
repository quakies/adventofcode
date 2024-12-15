class Guard:

    def __init__(self):
        self.ri = -1  # north/south increment
        self.ci = 0  # eat/west increment
        self.dir = 'north'
        self.pos_marker = '^'
        self.marker = '|'
        self.reset()


    def dump(self):
        print(f'Guard state: dir: {self.dir}, pos_marker: {self.pos_marker} ri: {self.ri}, ci: {self.ci}')


    def reset(self):
        self.ri = -1  # north/south increment
        self.ci = 0  # eat/west increment
        self.dir = 'north'
        self.pos_marker = '^'
        self.marker = '|'


    def turn(self):
        if self.dir == 'north':
            self.dir = 'east'
            self.ri = 0
            self.ci = 1
            self.pos_marker = '>'
            self.marker = '-'
        elif self.dir == 'east':
            self.dir = 'south'
            self.ri = 1
            self.ci = 0
            self.pos_marker = 'v'
            self.marker = '|'
        elif self.dir == 'south':
            self.dir = 'west'
            self.ri = 0
            self.ci = -1
            self.pos_marker = '<'
            self.marker = '_'
        else:  # 'west'
            self.dir = 'north'
            self.ri = -1
            self.ci = 0
            self.pos_marker = '^'
            self.marker = '|'

class Position:
    def __init__(self, r=0, c=0):
        self.r = r
        self.c = c

    def comp(self, pos):
        if self.r == pos.r and self.c == pos.c:
            return True
        return False

    def pp(self):
        return " ".join([str(self.r), str(self.c)])



class Grid:

    def __init__(self, g, start_pos):
        self.initial_grid = g
        self.start_pos = Position(start_pos[0], start_pos[1])

        self.grid = [[]]
        self.rows = 0
        self.cols = 0
        self.pos = Position()
        self.next_pos = Position()
        self.turns = []


    def reset(self):

        # reset the grid
        self.grid = []
        for l in self.initial_grid:
            self.grid.append(l[:])

        self.rows = len(self.grid)
        self.cols = len(self.grid[0])

        self.pos = Position(self.start_pos.r, self.start_pos.c)
        self.next_pos = Position()

        self.turns = []


    def dump_grid(self, message=''):

        print(f'Grid Dump: ', message)
        for i, l in enumerate(self.grid):
            print(f'{i} ', "".join(l))


    def add_obstruction(self, pos):
        self.grid[pos.r][pos.c]= 'O'

    def add_marker(self, pos, marker):
        self.grid[pos.r][pos.c]= marker


    def has_obstruction(self, pos):
        if self.grid[pos.r][pos.c] in ['#', 'O']:
            return True
        return False


    def get_next_pos(self, guard):
        self.next_pos.r = self.pos.r + guard.ri
        self.next_pos.c = self.pos.c + guard.ci


    def is_next_pos_off_grid(self):
        if self.next_pos.r < 0 or self.next_pos.r == self.rows:
            return True
        if self.next_pos.c < 0 or self.next_pos.c == self.cols:
            return True

        return False


    def is_next_pos_a_turn(self):
        if self.has_obstruction(self.next_pos):
            return True
        return False


    def turn(self, guard):
        self.add_marker(self.pos, '+')
        guard.turn()

        self.turns.append(Position(self.pos.r, self.pos.c))
        if len(self.turns) > 8:
            # only keep 8 items, so remove the first item
            self.turns = self.turns[1:8]

    def is_a_loop(self):
        # if the first four turn positions are equal to the last
        # four turn positions, then we are in a loop
        if len(self.turns) < 8:
            return False

        print(f'TURNS: {self.turns[0].pp()}  {self.turns[1].pp()}  {self.turns[2].pp()}   {self.turns[3].pp()} ')
        print(f'TURNS: {self.turns[4].pp()}  {self.turns[5].pp()}  {self.turns[6].pp()}   {self.turns[7].pp()} ')

        if self.turns[0].comp(self.turns[4]) and \
            self.turns[1].comp(self.turns[5]) and \
            self.turns[2].comp(self.turns[6]) and \
            self.turns[3].comp(self.turns[7]):
            return True
        return False



    def move_to_next_pos(self, guard):
        self.pos.r += guard.ri
        self.pos.c += guard.ci


    def walk_the_grid(self, guard):
        # this should return 1 if in a loop
        # 0 if walked off the grid

        ct = 0
        while True:
            ct += 1
            self.add_marker(self.pos, guard.marker)
            self.get_next_pos(guard)
            if self.is_next_pos_off_grid():
                return 0

            if self.is_next_pos_a_turn():
                self.turn(guard)
                if self.is_a_loop():
                    return 1
            else:
                self.move_to_next_pos(guard)
            self.dump_grid('LLLLLLLLLLLLLLLLLLLLLL')

    def looper(self, obstruction_pos):
        self.reset()
        self.add_obstruction(obstruction_pos)

        guard = Guard()

        return self.walk_the_grid(guard)


def get_iput(filename):
    g = []
    # Step 1: Read the file
    r = 0
    with open(filename, "r") as file:
        lines = file.readlines()
        start_pos = ()

        for line in lines:

            line = line.strip()
            g.append(list(line))
            if (tcol := line.find('^')) > 0:
                start_pos = (r, tcol)
            r += 1

        return g, start_pos


def main():
    g, start_pos = get_iput('input')

    grid = Grid(g, start_pos)
    grid.reset()

    grid.dump_grid('Initial')

    # test loops: [6,3] [7,6] [7,7] [8,1] [8,3] [9,7]
    loop_count = 0

    loop_count += grid.looper(Position(1,23))
    grid.dump_grid('TEST ')
    print(f'LOOPER COUNT ', loop_count)
    exit(0)


    # TODO LOOP GOES HERE
    for r in range(grid.rows):
        for c in range(grid.cols):
            print(f'LOOP r: {r}  c: {c}')
            grid.reset()
            loop_count += grid.looper(Position(r,c))
            print(f'loop count ', loop_count)
            #grid.dump_grid('Final')

    print(f'LOOPER COUNT ', loop_count)


main()
