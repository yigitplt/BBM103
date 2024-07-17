import sys

# this function creates a list of the txt file, taking every row as an item
def lister(input):
    content = input.readlines()
    rows = [[int(i) for i in row.split()] for row in content]
    return rows

# this function creates a table of numbers from the list of the rows
def unlister(alist):
    for row in alist:
        print(f"{' '.join(map(str, row))}")

# this function collects the location of the neighbor cell if it is equal to the selected number
def neighbor_finder(row, column, alist):
    neighbors = []

    # above and below neighbors
    for i in range(3):
        row_index = row + 1 - i
        if 0 <= row_index < len(alist) and i != 1 and alist[row][column] == alist[row_index][column]:
            neighbors.append((row_index, column))

    # left and right neighbors
    for a in range(3):
        column_index = column + 1 - a
        if 0 <= column_index < len(alist[row]) and a != 1 and alist[row][column] == alist[row][column_index]:
            neighbors.append((row, column_index))

    return neighbors


def collector(row, column, alist, neighbors):
    collected_nums = [(row, column)]    # locations of the collected numbers, the selected num is already added

    while len(neighbors) > 0:
        current_row, current_column = neighbors.pop()     # evaluate the last item in the neighbor list
        if (current_row, current_column) not in collected_nums:
            collected_nums.append((current_row, current_column))

            #add the location of the new neighbors to the neighbor list so we can find its neighbors and follow chain.
            new_neighbors = neighbor_finder(current_row, current_column, alist)
            for a in new_neighbors:
                if a not in collected_nums:
                    neighbors.append(a)

    # do not collect the number if no move can be made
    if len(collected_nums) == 1:
        collected_nums.remove((row, column))

    return collected_nums

def empty_column(alist):
    empty = True
    empty_columns = [i for i in range(len(alist[0]))]

    for col in range(len(alist[0])):
        for row in range(len(alist)):
            if alist[row][col] != " ":
                if col in empty_columns:
                    empty_columns.remove(col)

    return empty_columns


def eraser(alist, collected):
    for i in collected:
        alist[i[0]][i[1]] = " "

    # slides the numbers downwards if their below is empty
    for row in range(len(alist) - 1, 0, -1):
        for col in range(len(alist[row])):
            if alist[row][col] == " ":
                for i in range(row, -1, -1):
                    if alist[i][col] != " ":
                        alist[row][col] = alist[i][col]
                        alist[i][col] = " "
                        break


    # slides the columns leftwards if a column is empty
    empty_columns = empty_column(alist)
    if len(empty_columns) > 0:
        for i in empty_columns:
            if i != len(alist[0]) - 1:
                for line in alist:
                    for k in range(empty_columns[0], len(alist[0]) - 1):
                        temp = line[k]
                        line[k] = line[k + 1]
                        line[k + 1] = temp

    # deletes the top rows if they are empty
    empty_rows = []
    for rw in range(len(alist)):
        empty = True
        for cl in range(len(alist[rw])):
            if alist[rw][cl] != " ":
                empty = False
                break
        if empty:
            empty_rows.append(rw)

    for n in empty_rows:
        alist.remove(alist[0])

    # if the table is empty, adds a new line (according to piazza question @88_f11)
    if len(alist) == 0:
        print()

    a = unlister(alist)
    return a

# this func checks if there are any possible movements or not
def is_solved(row_list):
    for row in range(len(row_list)):
        for col in range(len(row_list[row])):
            if row_list[row][col] != " ":
                neighbors = neighbor_finder(row, col, row_list)
                collected = collector(row, col, row_list, neighbors)
                if len(collected) > 1:
                    return False
    return True

# this func calculates the points
def points(row, column, row_list, collected):
    point = 0

    selected_num =(row_list[row][column])
    if selected_num != " ":
        point += int(selected_num)*len(collected)
        return point


def printer(row, column, row_list, total):
    neighbors = neighbor_finder(row, column, row_list)
    collected = collector(row, column, row_list, neighbors)
    point = points(row, column, row_list, collected)
    total += point

    if len(collected) == 0:
        print("No movement happened try again\n")
    eraser(row_list, collected)
    print(f"\nYour score is: {total}\n")

    if is_solved(row_list):
        print("Game over")


    return total


def main():
    input_file = open(sys.argv[1], "r")
    row_list = lister(input_file)
    total = 0
    unlister(row_list)
    print("\nYour score is: 0\n")
    while not is_solved(row_list):
        user_value = input("Please enter a row and a column number: ")
        print()
        user_row = int(user_value[0]) - 1
        user_column = int(user_value[2]) - 1

        if not (0 <= user_row < len(row_list) and 0 <= user_column < len(row_list[0]) and row_list[user_row][user_column] != " "):
            print("Please enter a correct size!\n")
        else:
            total = printer(user_row, user_column, row_list, total)


if __name__ == "__main__":
    main()