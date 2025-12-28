import pathlib
import random
import typing as tp

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self,
        size: tp.Tuple[int, int],
        randomize: bool = True,
        max_generations: tp.Optional[float] = float("inf"),
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:

        grid = []

        for row in range(self.rows):
            current_row = []
            for col in range(self.cols):
                if randomize:
                    cell_value = random.randint(0, 1)
                else:
                    cell_value = 0
                current_row.append(cell_value)
            grid.append(current_row)

        return grid

    def get_neighbours(self, cell: Cell) -> Cells:
        row, col = cell
        neighbours = []

        for delta_row in [-1, 0, 1]:
            for delta_column in [-1, 0, 1]:
                if delta_row == 0 and delta_column == 0:
                    continue

                new_row = row + delta_row
                new_col = col + delta_column

                if 0 <= new_row < self.rows and 0 <= new_col < self.cols:
                    neighbours.append(self.curr_generation[new_row][new_col])

        return neighbours

    def get_next_generation(self) -> Grid:

        new_grid = self.create_grid(randomize=False)

        for row in range(self.rows):
            for col in range(self.cols):
                neighbours = self.get_neighbours((row, col))
                alive_neighbours = sum(neighbours)

                current_cell = self.curr_generation[row][col]

                if current_cell == 1:
                    if alive_neighbours == 2 or alive_neighbours == 3:
                        new_grid[row][col] = 1
                else:
                    if alive_neighbours == 3:
                        new_grid[row][col] = 1

        return new_grid

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        # Сохраняю текущее поколение как предыдущее
        self.prev_generation = self.curr_generation.copy()
        # Получаю следующее поколение
        self.curr_generation = self.get_next_generation()
        # Увеличиваю счетчик поколений
        self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        if self.max_generations is None:
            return False  # Если нет ограничения, то никогда не превышено
        return self.generations >= self.max_generations

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        return self.curr_generation != self.prev_generation

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        """
        Прочитать состояние клеток из указанного файла.
        """
        with open(filename, "r") as f:
            lines = f.readlines()
            # Определяю размеры сетки
            rows = len(lines)
            cols = len(lines[0].strip()) if lines else 0

            # Создаю игру с пустой сеткой
            game = GameOfLife((rows, cols), randomize=False)

            # Заполняю сетку из файла
            for i, line in enumerate(lines):
                line = line.strip()
                for j, char in enumerate(line):
                    game.curr_generation[i][j] = int(char)

            # Инициализирую предыдущее поколение
            game.prev_generation = game.create_grid(randomize=False)

        return game

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        with open(filename, "w") as f:
            for row in self.curr_generation:
                # Преобразую числа в строки и объединяю
                line = "".join(str(cell) for cell in row)
                f.write(line + "\n")
