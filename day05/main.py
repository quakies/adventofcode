# Adventofcode Day05 Challenge - Print Queue


def load_data():
    rules = {}
    update = []

    # Step 1: Read the file
    with open("input", "r") as file:
        lines = file.readlines()

        for line in lines:
            line = line.strip()
            if '|' in line:
                rule = list(map(int, line.split('|')))
                if rule[0] not in rules:
                    rules[rule[0]] = []
                rules[rule[0]].append(rule[1])

            elif ',' in line:
                update.append(list(map(int, line.split(','))))

        return rules, update


def check_update(update, rules):
    for a, b in zip(update, update[1:]):
        if a not in rules or b not in rules[a]:
            return 0

    # made it to here so must be an ok update
    # return the middle value
    middle = update[len(update) // 2]

    return middle

def part1(rules, updates):

    middle_number_sum = 0

    print(f'Day05 Challenge - Print Queue')
    failed_updates = []

    for update in updates:
        update_num = check_update(update, rules)
        if update_num == 0:
            failed_updates.append(update)

        middle_number_sum += check_update(update, rules)

    print(f'\n Part 1 middle number sum: ', middle_number_sum)

    return failed_updates

def fixit(update, rules):
    # Try to fix the updates that violate the ordering rules

    r = range(len(update))
    for i, j in zip(r, r[1:]):

        a = update[i]
        b = update[j]

        if a in rules and b in rules[a]:
            # skip it, the fixed value is OK
            pass
        else:   # swap the contents of i & j
            update[i] = b
            update[j] = a

    return update


def fff(update, rules):
    # Fix the update, maybe need to recurse down the items in the update
    # to get them in the correct order.

    update = fixit(update, rules)
    middle = check_update(update, rules)
    if middle > 0:
        return middle

    return fff(update,rules)


def part2(failed_updates, rules):
    # Fix the bad updates and sum the middle number

    print(f'\nPart 2: Fix {len(failed_updates)} failed updates')
    middle_number_sum = 0
    for update in failed_updates:
        middle_number_sum += fff(update, rules)

    print(f'\nPart 2 Fixed update middle number sum: ', middle_number_sum)


def main():
    rules, updates = load_data()

    failed_updates = part1(rules, updates)

    part2(failed_updates, rules)

main()