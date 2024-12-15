from dataclasses import dataclass, field
from typing import List


@dataclass
class Spot:
    r: int
    c: int
    elevation: int


@dataclass
class Trailhead:
    spot: Spot = field(default_factory=list)
    score: int = field(default=0, init=False)
    trail: List[Spot] = field(default_factory=list, init=False)


@dataclass
class Topo:
    topo: List[List[Spot]] = field(default_factory=list)
    trailheads: List[Trailhead] = field(default_factory=list)
    apexes: List[Trailhead] = field(default_factory=list)

    total_score: int = field(default=0, init=False)
    rmax: int = field(default=0, init=False)
    cmax: int = field(default=0, init=False)
    offsets: list = field(default_factory=list, init=False)

    def set_shape(self):
        self.rmax = len(self.topo)
        if self.rmax > 0:
            self.cmax = len(self.topo[0])

        self.offsets = [{'r': 0, 'c': -1}, {'r': 0, 'c': 1}, {'r': -1, 'c': 0}, {'r': 1, 'c': 0}]


    def find_trail(self, spot, trail, trailhead):

        if spot.elevation == 9:
            trailhead.score += 1
            return list()

        trail = trail + self.get_neighbors(spot)

        while trail:
            spot = trail.pop(0)
            self.find_trail(spot, trail, trailhead)


    # Outside the topo area, so no neighbors

    def get_neighbors(self, current_spot):
        nb = list()
        nb_elevation = current_spot.elevation + 1

        for offset in self.offsets:
            r = current_spot.r + offset['r']
            c = current_spot.c + offset['c']

            if r < 0 or r == self.rmax or \
                    c < 0 or c ==  self.cmax:
                # Outside the topo area, so no neighbors
                continue
            else:
                # get a neighbor

                spot = self.topo[r][c]
                if spot.elevation != nb_elevation:
                    # Not the next higher elevation, so skip it
                    continue

                nb.append(spot)

        return nb

    def find_trails(self):

        for trailhead in self.trailheads:
            self.find_trail(trailhead.spot, list(), trailhead)
            print(f'Find Trail {trailhead}')


def get_input(filename):
    data = list()
    trailheads = list()
    apexes = list()

    with open(filename, "r") as file:
        for r, line in enumerate(file.readlines()):
            row = list()
            for c, elevation in enumerate(list(map(int, line.strip()))):
                # Create a spot (map location)
                spot = Spot(r, c, elevation)
                row.append(spot)
                if elevation == 0:
                    # Keep track of trailheads
                    trailheads.append(Trailhead(spot))
                if elevation == 9:
                    # Keep track of end of trails (max elevation of 9)
                    apexes.append(Trailhead(spot))
            data.append(row)

    return data, trailheads, apexes


def main():
    data, trailheads, apexes = get_input('test-input')

    topo = Topo(data, trailheads, apexes)
    topo.set_shape()


    topo.find_trails()



    # topo.find_trails()

    print(f'Day 10 Challenge: Hoof It')
    print(f'-----------------------------------------')
    print(topo)


main()
