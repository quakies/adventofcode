# Adventofcode Main Part 2 - modification to code for Part 1

class Antinode:

    def __init__(self, r, c, ri, ci):
        self.r = r
        self.c = c
        self.ri = ri
        self.ci = ci



class Antenna:

    def __init__(self, freq):
        self.locations = []
        self.freq = freq
        self.antinodes = []
        self.tnodes = []


    def add_location(self, location):
        self.locations.append(location)


    def in_shape(self, loc, shape):
        if loc.r < 0 or loc.r > shape[0]:
            return False
        elif loc.c < 0 or loc.c > shape[1]:
            return False
        return True


    def loc_offset(self, shape, loc1, loc2):
        # Figure out where to put nodes
        rdiff = abs(loc1[0] - loc2[0])
        cd = loc1[1] - loc2[1]
        cdiff = abs(cd)

        if cd >= 0:
            an1 = Antinode(loc1[0] - rdiff,loc1[1] + cdiff, -rdiff, cdiff)
            an2 = Antinode(loc2[0] + rdiff, loc2[1] - cdiff, rdiff, -cdiff)
            #an1 = [loc1[0] - rdiff, loc1[1] + cdiff]
            #an2 = [loc2[0] + rdiff, loc2[1] - cdiff]
        else:
            an1 = Antinode(loc1[0] - rdiff, loc1[1] - cdiff, -rdiff, -cdiff)
            an2 = Antinode(loc2[0] + rdiff, loc2[1] + cdiff, rdiff, cdiff)
            #an1 = [loc1[0] - rdiff, loc1[1] - cdiff]
            #an2 = [loc2[0] + rdiff, loc2[1] + cdiff]

        if self.in_shape(an1, shape):
            self.antinodes.append(an1)
        if self.in_shape(an2, shape):
            self.antinodes.append(an2)


    def find_antinodes(self, shape):
        for i in range(len(self.locations)):
            for j in range(i + 1, len(self.locations)):
                self.loc_offset(shape, self.locations[i], self.locations[j])


        # Now find T-frequency
        for an in self.antinodes:
            an_tmp = Antinode(an.r + an.ri, an.c + an.ci, an.ri, an.ci)
            while True:
                if self.in_shape(an_tmp, shape):
                    self.tnodes.append(an_tmp)
                    an_tmp = Antinode(an_tmp.r+an.ri, an_tmp.c+an.ci, an_tmp.ri, an_tmp.ci)
                else:
                    break



    def dump(self, message=''):
        print(f'{message} Freq: {self.freq}, locations: ', self.locations)
        print(f'Antinodes: ', self.antinodes)


class Antennas:

    def __init__(self):
        self.antennas = {}
        self.shape = []


    def add_antenna_info(self, freq, location):
        if freq not in self.antennas:
            antenna = Antenna(freq)
            self.antennas[freq] = antenna
        self.antennas[freq].add_location(location)


    def find_antinodes(self):
        for freq, locations in self.antennas.items():
            self.antennas[freq].find_antinodes(self.shape)

    def collapse_antinodes(self):
        ddd = []
        for freq in self.antennas:
            for ans in self.antennas[freq].antinodes:
                ddd.append([ans.r, ans.c])

        for freq in self.antennas:
            for ans in self.antennas[freq].tnodes:
                ddd.append([ans.r, ans.c])

        for freq in self.antennas:
            for loc in self.antennas[freq].locations:
                ddd.append(loc)

        # Remove Duplicate locations
        fff = [list(x) for x in set(tuple(sublist) for sublist in ddd)]

        print(f'Antinode & Tnode Count: ', len(fff))

    def dump(self, message='Antennas'):
        for f, a in self.antennas.items():
            a.dump()


def get_input(filename):
    antennas = Antennas()

    with open(filename, "r") as file:
        lines = file.readlines()

        r = 0
        for r, l in enumerate(lines):
            for c, item in enumerate(list(l.strip())):
                if item != '.':
                    antennas.add_antenna_info(item, [r, c])

    antennas.shape = [r, c]
    return antennas


def main():
    print(f'Part 2 Day 8 Challenge')
    antennas = get_input('input')
    antennas.find_antinodes()
    antennas.collapse_antinodes()
    #antennas.dump()


main()
