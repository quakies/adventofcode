class Antenna:

    def __init__(self, freq):
        self.locations = []
        self.freq = freq
        self.antinodes = []


    def add_location(self, location):
        self.locations.append(location)


    def in_shape(self, loc, shape):
        if loc[0] < 0 or loc[0] > shape[0]:
            return False
        elif loc[1] < 0 or loc[1] > shape[1]:
            return False
        return True


    def loc_offset(self, shape, loc1, loc2):
        # TODO need to figure where to put nodes
        rdiff = abs(loc1[0] - loc2[0])
        cd = loc1[1] - loc2[1]
        cdiff = abs(cd)

        if cd >= 0:
            an1 = [loc1[0] - rdiff, loc1[1] + cdiff]
            an2 = [loc2[0] + rdiff, loc2[1] - cdiff]
        else:
            an1 = [loc1[0] - rdiff, loc1[1] - cdiff]
            an2 = [loc2[0] + rdiff, loc2[1] + cdiff]

        if self.in_shape(an1, shape):
            self.antinodes.append(an1)
        if self.in_shape(an2, shape):
            self.antinodes.append(an2)


    def find_antinodes(self, shape):
        for i in range(len(self.locations)):
            for j in range(i + 1, len(self.locations)):
                offset = self.loc_offset(shape, self.locations[i], self.locations[j])


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
                ddd.append(ans)

        fff = [list(x) for x in set(tuple(sublist) for sublist in ddd)]

        print(f'Antinode Count: ', len(fff))

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
    antennas = get_input('input')
    antennas.find_antinodes()
    antennas.collapse_antinodes()
    #antennas.dump()


main()
