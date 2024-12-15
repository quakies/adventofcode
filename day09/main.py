def is_even(num):
    return num % 2 == 0


def is_odd(num):
    return num % 2 != 0


class FragInfo:

    def __init__(self, size, index, id=0):
        self.id = id
        self.size = size
        self.index = index


class Disk:

    def __init__(self):
        # Even (including 0) is block size
        # Odd is space size

        self.disk_map = list()
        self.fragmented_disk = list()
        self.block_info = list()
        self.space_info = list()
        self.compacted_disk = list()
        self.compacted_better_disk = list()

        self.id = 0


    def build_fragmented_disk(self):
        disk_map = list(self.disk_map)
        index = 0
        for i, block_size in enumerate(self.disk_map):
            if is_even(i):
                # file block size - contains the file id in each block
                self.fragmented_disk.extend([self.id] * block_size)
                self.block_info.append(FragInfo(block_size, index, self.id))
                self.id += 1
            else:
                # space, denoted by '.'
                self.fragmented_disk.extend(['.'] * block_size)
                self.space_info.append(FragInfo(block_size, index))
            index += block_size


    def compact_disk(self):
        frag_disk = list(self.fragmented_disk)

        while len(frag_disk) > 0:
            if (left := frag_disk.pop(0)) != '.':
                self.compacted_disk.append(left)
            else:
                # Found a blank space, pick a block value from
                # end of list and put it in the blank space
                while len(frag_disk) > 0 and (right := frag_disk.pop()) == '.':
                    # pop the '.' off the end of this
                    pass
                # Should have a real vale
                self.compacted_disk.append(right)


    def compact_better(self):
        better = list(self.fragmented_disk)
        blocks = list(self.block_info)
        spaces = list(self.space_info)

        while len(blocks) > 0 and len(spaces) > 0:
            # Work backwards through the blocks
            block = blocks.pop()

            for index, space in enumerate(spaces):
                if block.size <= space.size:
                    # move block info to the space
                    better[space.index:space.index + block.size] = better[block.index:block.index + block.size]
                    # replace the original block location with spaces (really '.')
                    tlist = list(['.'] * block.size)
                    better[block.index:block.index + block.size] = tlist[:block.size]

                    if block.size == space.size:
                        # remove the space info since we can't use it
                        del spaces[index]
                    else:
                        # block didn't use all the space, so update the space info
                        space.size -= block.size
                        space.index += block.size

                    break

        self.compacted_better_disk = list(better)


    def checksum(self):

        chsum = 0
        for index, idnum in enumerate(self.compacted_disk):
            chsum += index * idnum

        return chsum


    def checksum_better(self):

        chsum = 0
        for index, idnum in enumerate(self.compacted_better_disk):
            if idnum != '.':
                chsum += index * idnum

        return chsum


    def dump(self):
        print(f'Disk map count: ', len(self.disk_map))
        print(self.disk_map)
        print(f'Fragmented count: ', len(self.fragmented_disk))
        print(self.fragmented_disk)
        print(f'Compacted count: ', len(self.compacted_disk))
        print(self.compacted_disk)
        print(f'Compacted Better count: ', len(self.compacted_better_disk))
        print(self.compacted_better_disk)

        # self.block_info_dump()
        # self.space_info_dump()


    def block_info_dump(self):
        t = list()
        for b in self.block_info:
            t.append(f'Index: {b.index}, size: {b.size}, ID: {b.id}')
        print(t)


    def space_info_dump(self):
        t = list()
        for b in self.space_info:
            t.append(f'Index: {b.index}, size: {b.size}')
        print(t)


def get_input(filename):
    disk = Disk()

    with open(filename, "r") as file:
        for line in file.readlines():
            disk.disk_map = list(map(int, str(line.strip())))

    return disk


def main():
    disk = get_input('input')

    print(f'Part 1 Defrag One')
    disk.build_fragmented_disk()
    disk.compact_disk()

    checksum = disk.checksum()
    print(f'Checksum: ', checksum)
    # NOTE: Part 1 checksum is 6356833654075

    # Not working.... not sure why. Did cheat a bit and got solution from
    # Reddit to see how far off I was -- alot...
    # Correct answer is 6389911791746
    print(f'\nPart 2 Defrag Two')
    disk.compact_better()

    #disk.dump()
    print(f'Disk Map Count: ', len(disk.disk_map))

    print(f'Compacted Better Count: ', len(disk.compacted_better_disk))

    checksum = disk.checksum_better()
    print(f'Checksum Better: ', checksum)


main()
