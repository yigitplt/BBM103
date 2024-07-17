import sys

# this function turns the given sudoku into a list, taking every row as an item
def line_separate(input):
    content = input.readlines()
    lines = [[int(i) for i in line.split()] for line in content]
    return lines

# this function turns a list into its original sudoku version and writes it into the output file
def list_to_sudoku(alist, output):
    for row in alist:
        output.write(f"{' '.join(map(str, row))}" + "\n")

# this function checks if the sudoku is solved or not
def is_solved(empty_cells):
    if len(empty_cells) == 0:
        return True
    else:
        return False

# this function determines the empty cells and adds them into a list
def empty_locations(lines):
    empty_list = []
    for i in range(9):
        for j in range(9):
            if lines[i][j] == 0:
                empty_list.append([i, j])
    return empty_list

def value_checker(row, column, sudoku):
    possible_values = [x for x in range(1, 10)]    # the list of possible values for the empty cell

    # check the row of the empty cell for possibilities
    for i in range(1, 10):
        if i in sudoku[row]:
            possible_values.remove(i)

    # check the column of the empty cell for possibilities
    for a in range(9):
        if sudoku[a][column] in possible_values:
            possible_values.remove(sudoku[a][column])

    # determine the upper left cell of the 3x3 subgrid and check possibilities by iterating
    if row < 3:
        subgrid_row = 0
    elif row < 6:
        subgrid_row = 3
    elif row < 9:
        subgrid_row = 6
    if column < 3:
        subgrid_column = 0
    elif column < 6:
        subgrid_column = 3
    elif column < 9:
        subgrid_column = 6

    for i in range(3):
        for j in range(3):
            if sudoku[subgrid_row + i][subgrid_column + j] in possible_values:
                possible_values.remove(sudoku[subgrid_row + i][subgrid_column + j])

    return possible_values

def replacer(sudoku, empty_list, output):
    changed = True
    step = 1
    while changed:
        changed = False    # if no change is made, this flag remains false and it exits the loop
        position = 0

        while position <= len(empty_list) - 1:
            row = empty_list[position][0]
            column = empty_list[position][1]
            possible_values = value_checker(row, column, sudoku)

            # if there is only one possibility, change "0" with the only item in possible_values
            if len(possible_values) == 1:
                sudoku[row][column] = possible_values[0]
                empty_list.remove([row, column])    # remove the location from the list where empty locations are shown
                position = 0    # if a cell is changed, start evaluating empty_cells from the start in case that an ambiguity changed after placement
                changed = True

                # write the current step into the output file
                output.write(f"Step {step} - {possible_values[0]} @ R{row + 1}C{column + 1}" + "\n")
                output.write(18*"-" + "\n")
                list_to_sudoku(sudoku, output)

                # to avoid new line at the end
                if not is_solved(empty_list):
                    output.write(18*"-" + "\n")
                else:
                    output.write(18*"-")

                step += 1

            else:
                position += 1    # if there is more than 1 possible value, move on to the next empty cell

    return sudoku

def main():
    input_file = open(sys.argv[1], "r")
    output_file = open(sys.argv[2], "w")
    empty_sudoku = line_separate(input_file)
    empty_cells = empty_locations(empty_sudoku)
    output_file.write(18*"-" + "\n")    # 18 lines on top of the output
    replacer(empty_sudoku, empty_cells, output_file)
    input_file.close()
    output_file.flush()
    output_file.close()

if __name__ == "__main__":
    main()


