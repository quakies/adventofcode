import re
import pandas as pd

def get_dataframe():
    # Load the input data into a pandas dataframe to make access
    # to column data easier

    # Step 1: Read the file
    with open("input", "r") as file:
        lines = file.readlines()

    # Step 2: Parse the lines into a list of lists
    data = [list(line.strip()) for line in lines]

    # Step 3: Create a DataFrame
    return pd.DataFrame(data)



def xmas_scan(str):
    # Scan string for the XMAS string and return the count
    pattern = re.compile('XMAS')
    return len(pattern.findall(str))

def xmas_counter(slist):
    # scan forward for xmas
    xmas_count = 0
    xmas_count += xmas_scan("".join(slist))

    # scan backward for xmas
    slist.reverse()
    xmas_count += xmas_scan("".join(slist))

    return xmas_count


def horizontal_count(df):
    # Count the XMAS strings in a horizontal line of text
    xmas_count = 0

    for _, row in df.iterrows():
        rlist = row.tolist()
        xmas_count += xmas_counter(rlist)

    return xmas_count


def vertical_count(df):
    # Count XMAS strings in a vertical line of text
    xmas_count = 0

    # iterate over columns and count the xmas strings
    for _, col in df.items():
        clist = col.tolist()
        xmas_count += xmas_counter(clist)

    return xmas_count


def init_shifted_row(row_len):
    # Init a list with spaces
    return [" "] * row_len



def diagonal_count(df, direction, incr):
    # Count XMAS string on the diagonals. Do this by shifting each successive
    # row to create columns that mimic the diagonals, then call vertical_count.
    # Basicly this: (. are place holders for space character in the pandas dataframe)
    #   ABC                  ABC                       ..ABC
    #   DEF  --> Diagonal \  .DEF     --> Diagonal /   .DEF
    #   GHI                  ..GHI                     GHI
    shifted_list = []
    row_count, col_count = df.shape

    if direction == '\\':
        offset = 0
    else:
        offset = row_count

    for index, drow in df.iterrows():
        offset += incr
        srow = init_shifted_row(int(row_count + col_count))

        for col, letter in drow.items():
            srow[offset + int(col)] = letter

        shifted_list.append(srow)
    # Create dataframe from list of shifted rows
    df = pd.DataFrame(shifted_list)
    ct = vertical_count(df)
    return ct


def part1(df):
    # Count all the XMAS strings that meet typical word search rules
    # that are in the input data.
    xmas_total = 0

    xmas_total += horizontal_count(df)
    xmas_total += vertical_count(df)
    xmas_total += diagonal_count(df, '\\', 1)
    xmas_total += diagonal_count(df, '/', -1)

    print(f'Part One Challenge ')
    print(f'XMAS Count is ', xmas_total)


def is_mas(str):

    if str == 'MAS' or str == 'SAM':
        return True

    return False

def part2(df):
    # Find the crossing MAS strings in the input data.
    # Look for X-MAS by looking at all positions in the grid from
    # 1,1 to row_count-1, col_count-1
    # So skipping the first & last row, and first & last column.
    # If the letter in the position is an A, then check to see if
    # the diagonals spell MAS.

    print(f'\n Part 2 Challenge')

    mas_count = 0
    row_count, col_count = df.shape

    for r in range(1, row_count-1):
        for c in range(1, col_count-1):
            letter = df.iat[r,c]
            if letter == 'A':
                # check for MAS
                t1 = ''.join([df.at[r-1,c-1], letter, df.at[r+1,c+1]])
                t2 = ''.join([df.at[r+1,c-1], letter, df.at[r-1,c+1]])

                if is_mas(t1) and is_mas(t2):
                    mas_count += 1

    print(f'X-MAX count: ', mas_count)

def main():
    df = get_dataframe()

    print(f'Day04 Challenge')
    part1(df)

    part2(df)


main()
