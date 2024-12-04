# Advent of Code Day 02 Challenge
# Find total number of safe reports in input data

import numpy as np


def check_direction(diffs):
    if np.all(diffs > 0):
        # all diffs > 0 then original array should be ascending
        print(f'Ascending')
        return True

    if np.all(diffs < 0):
        # all diffs < 0 then original array should be descending
        print(f'Descending')
        return True

    print(f'Bad direction')
    return False


def check_report(report):
    # A valid report must satisfy the two following conditions:
    #   * Adjacent numbers must differ by at least 1 and no more than 3
    #   * Need to check that all numbers in report are ascending or descending
    #     - in other words, check direction

    # Calc the diffs between each element in the array
    diffs = np.diff(report)

    abs_diffs = np.abs(diffs)
    if max(abs_diffs) > 3:
        return False

    if min(abs_diffs) < 1:
        return False

    if not check_direction(diffs):
        return False

    return True


def salvage_report(report):
    # The quick and dirty and surely not clever solution is to iterate
    # through the report, removing one element at a time, then check
    # the report. Not the most efficient but should work.
    i = 0
    while i < len(report):
        s_report = np.delete(report, i)
        if check_report(s_report):
            return True
        i += 1

    return False


def main():
    valid_report_count = 0
    salvaged_report_count = 0

    with open("input", "r") as file:
        for line in file:
            line = line.strip()
            report = np.fromstring(line, dtype=int, sep=" ")
            if check_report(report):
                valid_report_count += 1
            elif salvage_report(report):
                salvaged_report_count += 1

    print(f'Valid report count: ', valid_report_count)
    print(f'Salvaged report count: ', salvaged_report_count)
    print(f'Total valid report count: ', (valid_report_count + salvaged_report_count))


main()
