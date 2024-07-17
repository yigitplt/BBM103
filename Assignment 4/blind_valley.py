import sys

# Creates a dictionary of the restrictions in order to apply it to the code
def restriction(input):
    restrictions = dict()
    high_row = [int(i) for i in input.readline().split()]
    base_row = [int(i) for i in input.readline().split()]
    high_column = [int(i) for i in input.readline().split()]
    base_column = [int(i) for i in input.readline().split()]

    for i in range(len(high_row)):
        restrictions["row " + str(i + 1)] = (high_row[i], base_row[i])

    for i in range(len(high_column)):
        restrictions["column " + str(i + 1)] = (high_column[i], base_column[i])

    return restrictions

# creates a list of the table
def table_list(input):
    content = input.readlines()
    row_list = [[i for i in line.split()] for line in content]
    return row_list

# checks the neighbors of a cell
def check_neighbors(alist, row, col):
    l1 = ["N", "L", "R", "U", "D"]   # do not check for neighbors if the cell is one of these

    # above and below neighbors
    for i in range(3):
        r_index = row + 1 - i
        if 0 <= r_index < len(alist) and i != 1 and alist[row][col] not in l1 and alist[row][col] == alist[r_index][col]:
            return False

    # left and right neighbors
    for k in range(3):
        c_index = col + 1 - k
        if 0 <= c_index < len(alist[row]) and k != 1 and alist[row][col] not in l1 and alist[row][col] == alist[row][c_index]:
            return False

    return True

# checks if the restrictions are obeyed
def check_restrictions(alist, restrictions):

    # checks the rows
    current_row = 1
    for rw in alist:
        h_count = rw.count("H")
        b_count = rw.count("B")
        res = restrictions["row " + str(current_row)]
        if res != (h_count, b_count) and res != (-1, b_count) and res != (h_count, -1) and res != (-1, -1):
            return False
        current_row += 1

    # checks the columns
    for col1 in range(len(alist[0])):
        h_col = 0
        b_col = 0
        re = restrictions["column " + str(col1 + 1)]
        for row1 in range(len(alist)):
            if alist[row1][col1] == "H":
                h_col += 1
            elif alist[row1][col1] == "B":
                b_col += 1

        if re != (h_col, b_col) and re != (-1, b_col) and re != (h_col, -1) and re != (-1, -1):
            return False

    return True

# if we reach the final possibility (where every cell is N) it means there is no solution
def no_solution(path):
    for row in path:
        for cell in row:
            if cell != "N":
                return False
    return True


def placer(base, path, row, column, restrictions, x, y, output):

    # change the value of the cells
    if base[row][column] == "L":
        path[row][column], path[row][column + 1] = x, y
    elif base[row][column] == "U":
        path[row][column], path[row + 1][column] = x, y

    # Check neighbors after placement
    if not check_neighbors(path, row, column):
        return "Wrong"

    # Check restrictions after placement. If the conditions are met, write the solution and exit
    if check_restrictions(path, restrictions):
        r_index = 0
        for row in path:
            if r_index != len(path) - 1:
                output.write(f"{' '.join(row)}" + "\n")
            else:
                output.write(f"{' '.join(row)}")
                sys.exit()
            r_index += 1

    elif no_solution(path):
        output.write("No solution!")
        sys.exit()

    return path

# determines the next cell to evaluate
def next_cell(path, row, column):
    if column + 1 < len(path[0]):
        return row, column + 1
    else:
        if row + 1 < len(path):
            return row + 1, 0


def solver(base, path, row, column, restrictions, output, visited):

    # if you reach the end, go back
    if row == len(path) - 1 and column == len(path[0]) - 1:
        return

    # Check if the current state has been visited before
    if (tuple(map(tuple, path)), row, column) in visited:
        return

    visited.add((tuple(map(tuple, path)), row, column))

    next = next_cell(path, row, column)

    # backtracking
    path1 = placer(base, path, row, column, restrictions, "H", "B", output)
    if path1 is not "Wrong":
        solver(base, path1, next[0], next[1], restrictions, output, visited)

    path2 = placer(base, path, row, column, restrictions, "B", "H", output)
    if path2 is not "Wrong":
        solver(base, path2, next[0], next[1], restrictions, output, visited)

    path3 = placer(base, path, row, column, restrictions, "N", "N", output)
    if path3 is not "Wrong":
        solver(base, path3, next[0], next[1], restrictions, output, visited)



def main():
    input_file = open(sys.argv[1], "r")
    output_file = open(sys.argv[2], "w")
    restrictions = restriction(input_file)
    base1 = table_list(input_file)
    base2 = [row[:] for row in base1]
    visited = set()
    solver(base1, base2, 0, 0, restrictions, output_file, visited)



if __name__ == "__main__":
    main()