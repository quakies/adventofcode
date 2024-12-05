# Adventofcode Day03 Challenge
# find valid mul(a,b) statements in a jumble of characters,
# then do the multiplication and sum all the products.
import re


def get_input_data():
    with open("input", "r") as file:
        return file.read()


def mul(a, b):
    # This will be called by eval()
    return int(a) * int(b)


def part1(data):
    # Find the mul(a,b) statements in the data string,
    # then run and sum them

    pattern = re.compile('mul\(\d{1,3}\,\d{1,3}\)')
    multiplied_sum = 0
    found = pattern.findall(data)

    for f in found:
        # Eval the found mul(a,b) statement and sum products
        multiplied_sum += eval(f)

    print(f'Found {len(found)} mul(a,b) statements to process')
    print(f'Multiplied number total: ', multiplied_sum)


def part2(data):
    # Part 2 - Processing mul(a,b) that are preceded by do() instruction and
    # skip the mul(a,b) that are preceded by don't() instruction
    # What we know: The first instruction in the inout is a don't(),
    # so we will start with that.
    enabled_data = ''

    while len(data) > 0:
        # We are in a DO section, so find the next dont or end of data.
        index = data.find('don\'t()')
        if index == -1:
            # dont was not found, must be at end of data
            enabled_data = "".join([enabled_data, data])
            data = ""
        else:
            enabled_data = "".join([enabled_data, data[:index]])
            data = data[index:]

        # We are now in a DONT section, so find the next do,
        # then chop that off the front of data since we ignore DONT data
        index = data.find('do()')
        if index == -1:
            data = ''
        else:
            data = data[index:]

    return enabled_data


def main():
    data = get_input_data()

    print(f'\n--- Part 1 - Search all data and calc value -------')
    part1(data)

    print(f'\n--- Part 2 - Filter out the dont data nad calc value -------')
    data = part2(data)
    part1(data)

main()
