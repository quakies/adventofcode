from itertools import product


class Calibration:

    def __init__(self, result, num_list):
        self.result = result
        self.num_list = num_list
        self.operators = []
        self.valid = False
        self.part = ''
        self.operators = {
            'part1': ['+', '*'],
            'part2': ['+', '*', '|']
        }


    def calc_using_permutations(self, permutation, part='part1'):
        v = self.num_list[0]
        remaining_values = list(self.num_list[1:])

        for p in permutation:
            if p == '+':
                v = v + remaining_values.pop(0)
            elif p == '*':
                v = v * remaining_values.pop(0)
            else:
                # Concat
                v = int(str(v) + str(remaining_values.pop(0)))

        if v == self.result:
            self.valid = True
            self.part = part
            return True

        return False


    def find_operators(self, part):
        perms = self.get_permutations(part)

        if part == 'part1':
            for p in perms:
                if self.calc_using_permutations(p, part):
                    # Matched self.result, so stop permutation check
                    return

        else:
            for p in perms:
                if self.calc_using_permutations(p, part):
                    # Matched self.result, so stop permutation check
                    return


    def get_permutations(self, part):
        # Get permutations for operators
        repeat = len(self.num_list) - 1
        if repeat == 1:
            # only two items in num_list, so simple permutation
            if part == 'part1':
                # Part 1 with just two nums, so try to add or multiply
                return [['+'], ['*']]
            else:
                # Part2 with just two nums, just concat them since we already
                # tried to add and multiply in pass one
                return [['|']]

        op_list = self.operators[part]
        return list(product(op_list, repeat=repeat))


    def dump(self):
        print(f'Result: {self.result} Part: {self.part} Nums: {self.num_list}')


class Cals:
    # Handles a collection of Calibrations

    def __init__(self):
        self.calibrations = []
        self.max_num_count = 0


    def add(self, calibration):
        self.calibrations.append(calibration)
        self.max_num_count = max(self.max_num_count, len(calibration.num_list))


    def try_to_fix_equations(self):
        for c in self.calibrations:
            c.find_operators('part1')


    def try_to_fix_using_concat(self):
        for c in self.calibrations:
            if not c.valid:
                c.find_operators('part2')


    def total_cal_result(self):
        total = 0
        valid_count = 0
        for c in self.calibrations:
            if c.valid:
                total += c.result
                valid_count += 1
        return total, valid_count


    def dump(self, message='Equations'):

        print(f'{message}')
        for c in self.calibrations:
            c.dump()


def get_input(filename):
    cals = Cals()

    # Step 1: Read the file
    with open(filename, "r") as file:
        lines = file.readlines()

        for line in lines:
            line = line.strip()
            cval, rest = list(line.split(': '))
            num_list = list(map(int, rest.strip().split(" ")))
            #            list(map(int, line.split('|')))
            cals.add(Calibration(int(cval), num_list))

    return cals


def main():
    cals = get_input('input')

    print(f'Part 1: Bridge Repair')

    cals.dump()
    cals.try_to_fix_equations()

    print(f'Total number of equations: ', cals.max_num_count)
    part1_total, part1_valid_count = cals.total_cal_result()
    print(f'\nPart 1 Total Calibration Results: ', part1_total)
    print(f'Part 1 Total Valid Equations: ', part1_valid_count)

    # Part 2: Only need to process the items from part one that
    # are not valid, using three operators (=,*,|). The permutations
    # of the three operators will be bigger than part one, so
    # want to skip those.
    print(f'Part 2: || Operator, this will take a minute or two....')
    cals.try_to_fix_using_concat()
    part2_total, part2_valid_count = cals.total_cal_result()
    print(f'\nPart 2 Total Calibration Results: ', part2_total)
    print(f'Part 2 Total Valid Equations: ', part2_valid_count)


main()
