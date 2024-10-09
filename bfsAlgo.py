# 0: wall (#)
# 1: free (" ")
# start: start (A)
# finish: finish (B)


def translate_maze(file_name):
    maze = []
    for i in range(len(open(file_name).readlines())):
        list = []
        for cell in open(file_name).readlines()[i]:
            match cell:
                case "#":
                    list.append("0")
                case " ":
                    list.append("1")
                case "A":
                    list.append("s")
                case "B":
                    list.append("f")
        maze.append(list)
    return maze


maze = translate_maze('maze4.txt')
mazeX = len(maze[0])
mazeY = len(maze)


def value_from_coord(coord, matrix):
    return matrix[coord[1]][coord[0]]


def find_start(matrix):
    list = []
    for i in range(len(matrix)):
        for n in range(len(matrix[i])):
            if matrix[i][n] == "s":
                list.append(n)
                list.append(i)
    return list


def find_end(matrix):
    list = []
    for i in range(len(matrix)):
        for n in range(len(matrix[i])):
            if matrix[i][n] == "f":
                list.append(n)
                list.append(i)
    return list


def print_maze(matrix):
    for i in range(len(matrix)):
        print(matrix[i])


def num_nodes(matrix):
    count = 0
    for r in matrix:
        for v in r:
            match v:
                case "1":
                    count += 1
                case "f":
                    count += 1
                case "v":
                    count += 1
    return count


def find_neighbors(coords, matrix):
    psbl = [[coords[0] + 1, coords[1]], [coords[0] - 1, coords[1]], [coords[0], coords[1] + 1],
            [coords[0], coords[1] - 1]]
    neighbors = []
    for coord in psbl:
        if (coord[0] >= mazeX) or (coord[1] >= mazeY):
            continue
        else:
            value = value_from_coord(coord, maze)
            if value == "1" or value == "f":
                neighbors.append(coord)
    return neighbors


def manh_dist(coords, matrix):
    end_x = find_end(matrix)[0]
    end_y = find_end(matrix)[1]
    return abs(coords[0] - end_x) + abs(coords[1] - end_y)


def filter_visited(queue, visited):
    for queued in queue:
        for coord in visited:
            if queued == coord:
                try:
                    queue.remove(coord)
                except ValueError:
                    continue
    return queue


def print_maze_alt(matrix):
    list = []
    for r in matrix:
        row = []
        for v in r:
            match v:
                case "0":
                    v = "⬛"
                case "1":
                    v = "⬜"
                case "s":
                    v = "🟥"
                case "f":
                    v = "🟩"
            row.append(v)
        list.append(row)
        print(*row)
    return list


def print_solved_maze(visited, matrix):
    for coord in visited:
        if matrix[coord[1]][coord[0]] == "s":
            continue
        else:
            matrix[coord[1]][coord[0]] = "v"
    for r in matrix:
        row = []
        for v in r:
            block = 0
            match v:
                case "0":
                    block = "⬛"
                case "1":
                    block = "⬜"
                case "v":
                    block = "🟧"
                case "s":
                    block = "🟥"
                case "f":
                    block = "🟩"
            row.append(block)
        print(*row)


def solve_maze(matrix):
    queue = []
    visited = []
    current_pos = find_start(maze)
    while current_pos != find_end(maze):
        neighbors = find_neighbors(current_pos, matrix)
        for neighbor in neighbors:
            queue.append(neighbor)
        queue = filter_visited(queue, visited)
        if len(queue) == 0:
            print("No solution.")
            break

        visited.append(current_pos)
        current_pos = queue[0]
        queue.pop(0)
        if current_pos == find_end(matrix):
            print_solved_maze(visited, matrix)
            print("Solution found at: " + current_pos.__str__())
            print("Nodes visited: " + len(visited).__str__() + " out of " + num_nodes(maze).__str__())
            break


solve_maze(maze)

""" 
- start at starting coordinate
- find neighbor(s)
- add neighbor(s) to queue
- using queue logic, pick next coord
- check if coord is goal
- if not, add coord to 'visited' list
- repeat!
"""
