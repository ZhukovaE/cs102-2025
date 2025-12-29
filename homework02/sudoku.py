import pathlib
import random
import typing as tp

T = tp.TypeVar("T")


def read_sudoku(path: tp.Union[str, pathlib.Path]) -> tp.List[tp.List[str]]:
    """Прочитать Судоку из указанного файла"""
    path = pathlib.Path(path)
    with path.open() as f:
        puzzle = f.read()
    return create_grid(puzzle)


def create_grid(puzzle: str) -> tp.List[tp.List[str]]:
    digits = [c for c in puzzle if c in "123456789."]
    grid = group(digits, 9)
    return grid


def display(grid: tp.List[tp.List[str]]) -> None:
    """Вывод Судоку"""
    width = 2
    line = "+".join(["-" * (width * 3)] * 3)
    for row in range(9):
        print("".join(grid[row][col].center(width) + ("|" if str(col) in "25" else "") for col in range(9)))
        if str(row) in "25":
            print(line)
    print()


def group(values: tp.List[T], n: int) -> tp.List[tp.List[T]]:
    """
    Сгруппировать значения values в список, состоящий из списков по n элементов
    >>> group([1,2,3,4], 2)
    [[1, 2], [3, 4]]
    >>> group([1,2,3,4,5,6,7,8,9], 3)
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    """
    return [values[i : i + n] for i in range(0, len(values), n)]


def get_row(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения для номера строки, указанной в pos
    >>> get_row([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '2', '.']
    >>> get_row([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (1, 0))
    ['4', '.', '6']
    >>> get_row([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (2, 0))
    ['.', '8', '9']
    """
    row_index = pos[0]
    return grid[row_index]


def get_col(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения для номера столбца, указанного в pos
    >>> get_col([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '4', '7']
    >>> get_col([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (0, 1))
    ['2', '.', '8']
    >>> get_col([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (0, 2))
    ['3', '6', '9']
    """
    result = [i[pos[1]] for i in grid]
    return result


def get_block(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения из квадрата, в который попадает позиция pos
    >>> grid = read_sudoku('puzzle1.txt')
    >>> get_block(grid, (0, 1))
    ['5', '3', '.', '6', '.', '.', '.', '9', '8']
    >>> get_block(grid, (4, 7))
    ['.', '.', '3', '.', '.', '1', '.', '.', '6']
    >>> get_block(grid, (8, 8))
    ['2', '8', '.', '.', '.', '5', '.', '7', '9']
    """
    row, col = pos
    start_row = (row // 3) * 3
    start_col = (col // 3) * 3

    block = []
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            block.append(grid[i][j])
    return block


def find_empty_positions(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.Tuple[int, int]]:
    """Найти первую свободную позицию в пазле
    >>> find_empty_positions([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']])
    (0, 2)
    >>> find_empty_positions([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']])
    (1, 1)
    >>> find_empty_positions([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']])
    (2, 0)
    """
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col] == ".":
                return (row, col)
    return None


def find_possible_values(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.Set[str]:
    """Вернуть множество возможных значения для указанной позиции
    >>> grid = read_sudoku('puzzle1.txt')
    >>> values = find_possible_values(grid, (0,2))
    >>> values == {'1', '2', '4'}
    True
    >>> values = find_possible_values(grid, (4,7))
    >>> values == {'2', '5', '9'}
    True
    """
    row_values = get_row(grid, pos)
    col_values = get_col(grid, pos)
    block_values = get_block(grid, pos)

    used_values = set(row_values) | set(col_values) | set(block_values)
    all_values = set("123456789")
    possible = all_values - used_values
    return possible


def solve(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.List[tp.List[str]]]:
    """Решение пазла, заданного в grid"""
    """ Как решать Судоку?
        1. Найти свободную позицию
        2. Найти все возможные значения, которые могут находиться на этой позиции
        3. Для каждого возможного значения:
            3.1. Поместить это значение на эту позицию
            3.2. Продолжить решать оставшуюся часть пазла
    >>> grid = read_sudoku('puzzle1.txt')
    >>> solve(grid)
    [['5', '3', '4', '6', '7', '8', '9', '1', '2'], ['6', '7', '2', '1', '9', '5', '3', '4', '8'], ['1', '9', '8', '3', '4', '2', '5', '6', '7'], ['8', '5', '9', '7', '6', '1', '4', '2', '3'], ['4', '2', '6', '8', '5', '3', '7', '9', '1'], ['7', '1', '3', '9', '2', '4', '8', '5', '6'], ['9', '6', '1', '5', '3', '7', '2', '8', '4'], ['2', '8', '7', '4', '1', '9', '6', '3', '5'], ['3', '4', '5', '2', '8', '6', '1', '7', '9']]
    """
    empty = find_empty_positions(grid)

    if empty is None:
        return grid

    row, col = empty

    possible_values = find_possible_values(grid, empty)

    for value in possible_values:

        grid[row][col] = value

        result = solve(grid)

        if result:
            return result

        grid[row][col] = "."

    return None


def check_solution(solution: tp.List[tp.List[str]]) -> bool:
    """ Если решение solution верно, то вернуть True, в противном случае False
    >> > correct_solution = [ \
        ['5', '3', '4', '6', '7', '8', '9', '1', '2'], \
        ['6', '7', '2', '1', '9', '5', '3', '4', '8'], \
        ['1', '9', '8', '3', '4', '2', '5', '6', '7'], \
        ['8', '5', '9', '7', '6', '1', '4', '2', '3'], \
        ['4', '2', '6', '8', '5', '3', '7', '9', '1'], \
        ['7', '1', '3', '9', '2', '4', '8', '5', '6'], \
        ['9', '6', '1', '5', '3', '7', '2', '8', '4'], \
        ['2', '8', '7', '4', '1', '9', '6', '3', '5'], \
        ['3', '4', '5', '2', '8', '6', '1', '7', '9']]
    >> > check_solution(correct_solution)
    True

    >> > wrong_solution1 = [ \
        ['5', '3', '4', '6', '7', '8', '9', '1', '2'], \
        ['6', '7', '2', '1', '9', '5', '3', '4', '8'], \
        ['1', '9', '8', '3', '4', '2', '5', '6', '7'], \
        ['8', '5', '9', '7', '6', '1', '4', '2', '3'], \
        ['4', '2', '6', '8', '5', '3', '7', '9', '1'], \
        ['7', '1', '3', '9', '2', '4', '8', '5', '6'], \
        ['9', '6', '1', '5', '3', '7', '2', '8', '4'], \
        ['2', '8', '7', '4', '1', '9', '6', '3', '5'], \
        ['3', '4', '5', '2', '8', '6', '1', '7', '8']]  # последняя цифра должна быть 9, а не 8
    >> > check_solution(wrong_solution1)
    False

    >> > wrong_solution2 = [ \
        ['1', '2', '3', '4', '5', '6', '7', '8', '9'], \
        ['1', '2', '3', '4', '5', '6', '7', '8', '9'], \
        ['1', '2', '3', '4', '5', '6', '7', '8', '9'], \
        ['1', '2', '3', '4', '5', '6', '7', '8', '9'], \
        ['1', '2', '3', '4', '5', '6', '7', '8', '9'], \
        ['1', '2', '3', '4', '5', '6', '7', '8', '9'], \
        ['1', '2', '3', '4', '5', '6', '7', '8', '9'], \
        ['1', '2', '3', '4', '5', '6', '7', '8', '9'], \
        ['1', '2', '3', '4', '5', '6', '7', '8', '9']]  # все строки одинаковые
    >> > check_solution(wrong_solution2)
    False

    >> > wrong_solution3 = [ \
        ['5', '3', '4', '6', '7', '8', '9', '1', '2'], \
        ['6', '7', '2', '1', '9', '5', '3', '4', '8'], \
        ['1', '9', '8', '3', '4', '2', '5', '6', '7'], \
        ['8', '5', '9', '7', '6', '1', '4', '2', '3'], \
        ['4', '2', '6', '8', '5', '3', '7', '9', '1'], \
        ['7', '1', '3', '9', '2', '4', '8', '5', '6'], \
        ['9', '6', '1', '5', '3', '7', '2', '8', '4'], \
        ['2', '8', '7', '4', '1', '9', '6', '3', '5'], \
        ['3', '4', '5', '2', '8', '6', '1', '7', '.']]  # есть пустая клетка
    >> > check_solution(wrong_solution3)
    False
    """

    for row in range(9):
        current_row = get_row(solution, (row, 0))
        if set(current_row) != set("123456789"):
            return False

    for col in range(9):
        current_col = get_col(solution, (0, col))
        if set(current_col) != set("123456789"):
            return False

    for row in range(0, 9, 3):
        for col in range(0, 9, 3):
            block = get_block(solution, (row, col))
            if set(block) != set("123456789"):
                return False

    return True


def generate_sudoku(N: int) -> tp.List[tp.List[str]]:
    """Генерация судоку заполненного на N элементов
    >>> grid = generate_sudoku(40)
    >>> sum(1 for row in grid for e in row if e == '.')
    41
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(1000)
    >>> sum(1 for row in grid for e in row if e == '.')
    0
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(0)
    >>> sum(1 for row in grid for e in row if e == '.')
    81
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    """
    count = max(0, min(N, 81))

    # Генерирую базовое решение алгоритмически
    base: tp.List[tp.List[str]] = []
    for row in range(9):
        base_row: tp.List[str] = []
        for col in range(9):
            # Формула для создания валидного судоку
            value = (row * 3 + row // 3 + col) % 9 + 1
            base_row.append(str(value))
        base.append(base_row)

    # Случайная перестановка цифр
    digits = list("123456789")
    random.shuffle(digits)
    digit_map = {str(i + 1): digits[i] for i in range(9)}

    # Применяю перестановку к базовому решению
    grid: tp.List[tp.List[str]] = []
    for row in range(9):
        new_row: tp.List[str] = []
        for col in range(9):
            new_row.append(digit_map[base[row][col]])
        grid.append(new_row)

    # Перемешиваю строки внутри вертикальных блоков
    for block in range(3):
        rows_in_block = list(range(block * 3, block * 3 + 3))
        random.shuffle(rows_in_block)

        for position in range(3):
            current_row_index = block * 3 + position
            new_row_index = rows_in_block[position]
            # Меняю целые строки местами
            temp_row = grid[current_row_index]
            grid[current_row_index] = grid[new_row_index]
            grid[new_row_index] = temp_row

    # Перемешиваю столбцы внутри горизонтальных блоков
    for block in range(3):
        cols_in_block = list(range(block * 3, block * 3 + 3))
        random.shuffle(cols_in_block)

        for position in range(3):
            current_col_index = block * 3 + position
            new_col_index = cols_in_block[position]
            if current_col_index != new_col_index:
                for row_index in range(9):
                    # Меняю значения в столбцах
                    temp_value = grid[row_index][current_col_index]
                    grid[row_index][current_col_index] = grid[row_index][new_col_index]
                    grid[row_index][new_col_index] = temp_value

    # Удаляю ячейки для создания головоломки
    cells_to_remove = 81 - count

    all_positions = [(row, col) for row in range(9) for col in range(9)]
    random.shuffle(all_positions)

    for cell_index in range(min(cells_to_remove, 81)):
        row, col = all_positions[cell_index]
        grid[row][col] = "."

    return grid


if __name__ == "__main__":
    for fname in ["puzzle1.txt", "puzzle2.txt", "puzzle3.txt"]:
        grid = read_sudoku(fname)
        display(grid)
        solution = solve(grid)
        if not solution:
            print(f"Puzzle {fname} can't be solved")
        else:
            display(solution)
