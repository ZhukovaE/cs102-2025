from copy import deepcopy
from random import choice, randint
from typing import List, Optional, Tuple, Union

import pandas as pd


def create_grid(rows: int = 15, cols: int = 15) -> List[List[Union[str, int]]]:
    return [["■"] * cols for _ in range(rows)]


def remove_wall(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param coord:
    :return:
    """
    x, y = coord

    direction = choice(["up", "right"])

    if direction == "up" and x - 2 < 0:
        direction = "right"
    elif direction == "right" and y + 2 >= len(grid[0]):
        direction = "up"

    if direction == "up":
        if x - 2 >= 0:
            grid[x - 1][y] = " "
    elif direction == "right":
        if y + 2 < len(grid[0]):
            grid[x][y + 1] = " "

    return grid


def bin_tree_maze(rows: int = 15, cols: int = 15, random_exit: bool = True) -> List[List[Union[str, int]]]:
    """

    :param rows:
    :param cols:
    :param random_exit:
    :return:
    """

    grid = create_grid(rows, cols)
    empty_cells = []
    for x, row in enumerate(grid):
        for y, _ in enumerate(row):
            if x % 2 == 1 and y % 2 == 1:
                grid[x][y] = " "
                empty_cells.append((x, y))

    # 1. выбрать любую клетку
    # 2. выбрать направление: наверх или направо.
    # Если в выбранном направлении следующая клетка лежит за границами поля,
    # выбрать второе возможное направление
    # 3. перейти в следующую клетку, сносим между клетками стену
    # 4. повторять 2-3 до тех пор, пока не будут пройдены все клетки
    for cell in empty_cells:
        grid = remove_wall(grid, cell)
    # генерация входа и выхода
    if random_exit:
        x_in, x_out = randint(0, rows - 1), randint(0, rows - 1)
        y_in = randint(0, cols - 1) if x_in in (0, rows - 1) else choice((0, cols - 1))
        y_out = randint(0, cols - 1) if x_out in (0, rows - 1) else choice((0, cols - 1))
    else:
        x_in, y_in = 0, cols - 2
        x_out, y_out = rows - 1, 1

    grid[x_in][y_in], grid[x_out][y_out] = "X", "X"

    return grid


def get_exits(grid: List[List[Union[str, int]]]) -> List[Tuple[int, int]]:
    """

    :param grid:
    :return:
    """
    exits = []

    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if cell == "X":
                exits.append((i, j))

    return exits


def make_step(grid: List[List[Union[str, int]]], k: int) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param k:
    :return:
    """
    new_grid = [row.copy() for row in grid]

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == k:

                if i > 0 and grid[i - 1][j] == 0:
                    new_grid[i - 1][j] = k + 1

                if i < len(grid) - 1 and grid[i + 1][j] == 0:
                    new_grid[i + 1][j] = k + 1

                if j > 0 and grid[i][j - 1] == 0:
                    new_grid[i][j - 1] = k + 1

                if j < len(grid[0]) - 1 and grid[i][j + 1] == 0:
                    new_grid[i][j + 1] = k + 1

    return new_grid


def shortest_path(
        grid: List[List[Union[str, int]]], exit_coord: Tuple[int, int]
) -> Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]:
    """

    :param grid:
    :param exit_coord:
    :return:
    """
    x, y = exit_coord

    cell_value = grid[x][y]

    if not isinstance(cell_value, int) or cell_value <= 0:
        return None

    path = []
    current_x, current_y = x, y
    current_value = cell_value

    while current_value > 1:
        path.append((current_x, current_y))

        if current_x > 0:
            neighbor = grid[current_x - 1][current_y]
            if isinstance(neighbor, int) and neighbor == current_value - 1:
                current_x -= 1
                current_value -= 1
                continue

        if current_x < len(grid) - 1:
            neighbor = grid[current_x + 1][current_y]
            if isinstance(neighbor, int) and neighbor == current_value - 1:
                current_x += 1
                current_value -= 1
                continue

        if current_y > 0:
            neighbor = grid[current_x][current_y - 1]
            if isinstance(neighbor, int) and neighbor == current_value - 1:
                current_y -= 1
                current_value -= 1
                continue

        if current_y < len(grid[0]) - 1:
            neighbor = grid[current_x][current_y + 1]
            if isinstance(neighbor, int) and neighbor == current_value - 1:
                current_y += 1
                current_value -= 1
                continue

        return None

    path.append((current_x, current_y))
    return path


def encircled_exit(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> bool:
    """

    :param grid:
    :param coord:
    :return:
    """
    x, y = coord
    rows = len(grid)
    cols = len(grid[0])

    if x == 0 and y == 0:
        if grid[x][y + 1] == "■" and grid[x + 1][y] == "■":
            return True
        else:
            return False
    elif x == 0 and y == cols - 1:
        if grid[0][cols - 2] == "■" and grid[1][cols - 1] == "■":
            return True
        return False
    elif x == rows - 1 and y == 0:
        if grid[rows - 1][1] == "■" and grid[rows - 2][0] == "■":
            return True
        return False
    elif x == rows - 1 and y == cols - 1:
        if grid[rows - 1][cols - 2] == "■" and grid[rows - 2][cols - 1] == "■":
            return True
        return False
    elif x == 0:
        if grid[0][y - 1] == "■" and grid[0][y + 1] == "■" and grid[1][y] == "■":
            return True
        return False
    elif x == rows - 1:
        if grid[rows - 1][y - 1] == "■" and grid[rows - 1][y + 1] == "■" and grid[rows - 2][y] == "■":
            return True
        return False
    elif y == 0:
        if grid[x - 1][0] == "■" and grid[x + 1][0] == "■" and grid[x][1] == "■":
            return True
        return False
    elif y == cols - 1:
        if grid[x - 1][cols - 1] == "■" and grid[x + 1][cols - 1] == "■" and grid[x][cols - 2] == "■":
            return True
        return False
    else:
        if 0 < x < rows - 1 and 0 < y < cols - 1:
            return False
    return False


def solve_maze(
        grid: List[List[Union[str, int]]],
) -> Tuple[List[List[Union[str, int]]], Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]]:
    """

    :param grid:
    :return:
    """
    exits = get_exits(grid)

    if len(exits) == 0:
        return grid, None

    if len(exits) == 1:
        return grid, exits[0]

    if len(exits) != 2:
        return grid, None

    exit1, exit2 = exits[0], exits[1]

    if encircled_exit(grid, exit1) or encircled_exit(grid, exit2):
        return grid, None

    wave_grid = [row.copy() for row in grid]

    for i in range(len(wave_grid)):
        for j in range(len(wave_grid[0])):
            if wave_grid[i][j] == " ":
                wave_grid[i][j] = 0
            elif wave_grid[i][j] == "X":
                wave_grid[i][j] = 0

    wave_grid[exit1[0]][exit1[1]] = 1

    k = 1
    max_steps = len(wave_grid) * len(wave_grid[0])

    for _ in range(max_steps):
        if wave_grid[exit2[0]][exit2[1]] != 0:
            break

        wave_grid = make_step(wave_grid, k)
        k += 1

    path = shortest_path(wave_grid, exit2)

    return wave_grid, path


def add_path_to_grid(
        grid: List[List[Union[str, int]]], path: Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]
) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param path:
    :return:
    """

    if path:
        for i, row in enumerate(grid):
            for j, _ in enumerate(row):
                if (i, j) in path:
                    grid[i][j] = "X"
    return grid


if __name__ == "__main__":
    print(pd.DataFrame(bin_tree_maze(15, 15)))
    GRID = bin_tree_maze(15, 15)
    print(pd.DataFrame(GRID))
    _, PATH = solve_maze(GRID)
    MAZE = add_path_to_grid(GRID, PATH)
    print(pd.DataFrame(MAZE))
