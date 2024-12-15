import math


def is_even(num):
    return num % 2 == 0


def num_len(num) -> int:
    if num == 0:
        return 1
    return int(math.log10(abs(num))) + 1


def rule_2(stone) -> list[int]:
    s = str(stone)
    i = len(s) // 2
    return [int(s[:i]), int(s[i:])]


def apply_rules(stone) -> list[int]:
    if stone == 0:
        # Rule One
        return [1]
    elif is_even(len(str(stone))):
        # Rule Two
        return rule_2(stone)

    # Rule Three - Default
    return [stone * 2024]


def main(stones, blinks):
    """Brute force solution to part one. Runs for a few minutes, thanks
       to the exponential growth of the data when the rules are applied
       """
    changed_stones = list(stones)
    for blink in range(blinks):
        t = list()
        for stone in changed_stones:
            cstone = apply_rules(stone)
            t = t + cstone
        changed_stones = t

    print(f'Changed stones after blinking {blink} times:')
    print(f'Stone count and final answer: {len(changed_stones)}')


def parse_input_file(file) -> list[int]:
    """Return a 2D-list of ints parsed from the given file."""
    with open(file, "r") as f:
        lines = f.readlines()

    return list(map(int, lines[0].strip().split(' ')))


if __name__ == "__main__":
    import argparse
    from pathlib import Path

    parser = argparse.ArgumentParser()
    parser.add_argument("input_file")
    parser.add_argument("blinks")

    args = parser.parse_args()

    stones = parse_input_file(Path(args.input_file))

    total_score = main(stones, int(args.blinks))
    print(f"Part One Score: Blink count {args.blinks}")

