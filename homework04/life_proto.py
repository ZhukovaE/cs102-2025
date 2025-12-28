import random
import typing as tp

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(self, width: int = 640, height: int = 480, cell_size: int = 10, speed: int = 10) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed

        self.grid = self.create_grid(randomize=True)

    def draw_lines(self) -> None:
        """Отрисовать сетку"""
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def run(self, grid: Grid) -> None:
        """Запустить игру"""
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        # Создаю списка клеток
        self.grid = self.create_grid(randomize=True)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Очищаю экран каждый кадр
            self.screen.fill(pygame.Color("white"))

            # Рисую сетку
            self.draw_lines()

            # Отрисовка списка клеток
            self.draw_grid()

            # Выполненяю один шаг игры
            self.grid = self.get_next_generation()

            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def create_grid(self, randomize: bool = False) -> Grid:
        """
        Создание списка клеток.

        Клетка считается живой, если ее значение равно 1, в противном случае клетка
        считается мертвой, то есть, ее значение равно 0.

        Parameters
        ----------
        randomize : bool
            Если значение истина, то создается матрица, где каждая клетка может
            быть равновероятно живой или мертвой, иначе все клетки создаются мертвыми.

        Returns
        ----------
        out : Grid
            Матрица клеток размером `cell_height` х `cell_width`.
        """
        grid = []  # Создаю пустой список для матрицы

        for row in range(self.cell_height):  # Прохожу по всем строкам
            current_row = []  # Создаю новую строку
            for col in range(self.cell_width):  # Прохожу по всем столбцам
                if randomize:
                    # Случайное значение: 0 (мертвая) или 1 (живая)
                    cell_value = random.randint(0, 1)
                else:
                    # Все клетки мертвые
                    cell_value = 0
                current_row.append(cell_value)  # Добавляю клетку в строку
            grid.append(current_row)  # Добавляю строку в матрицу

        return grid

    def draw_grid(self) -> None:
        """
        Отрисовка списка клеток с закрашиванием их в соответствующе цвета.
        """
        for row in range(self.cell_height):  # Прохожу по всем строкам
            for col in range(self.cell_width):  # Прохожу по всем столбцам
                # Определяю цвет в зависимости от состояния клетки
                if self.grid[row][col] == 1:  # Если клетка живая
                    color = pygame.Color("green")
                else:  # Если клетка мертвая
                    color = pygame.Color("white")

                # Вычисляю координаты прямоугольника для клетки
                x = col * self.cell_size  # X-координата = номер столбца * размер клетки
                y = row * self.cell_size  # Y-координата = номер строки * размер клетки

                # Создаю прямоугольник
                rect = pygame.Rect(x, y, self.cell_size, self.cell_size)

                # Рисую закрашенный прямоугольник
                pygame.draw.rect(self.screen, color, rect)

    def get_neighbours(self, cell: Cell) -> Cells:
        """
        Вернуть список соседних клеток для клетки `cell`.

        Соседними считаются клетки по горизонтали, вертикали и диагоналям,
        то есть, во всех направлениях.

        Parameters
        ----------
        cell : Cell
            Клетка, для которой необходимо получить список соседей. Клетка
            представлена кортежем, содержащим ее координаты на игровом поле.

        Returns
        ----------
        out : Cells
            Список соседних клеток.
        """
        row, col = cell
        neighbours = []  # Список для хранения соседей

        # Проверяю все 8 возможных направлений
        for delta_row in [
            -1,
            0,
            1,
        ]:  # Изменение по строке: -1 (вверх), 0 (та же строка), 1 (вниз)
            for delta_column in [
                -1,
                0,
                1,
            ]:  # Изменение по столбцу: -1 (влево), 0 (тот же столбец), 1 (вправо)
                # Пропускаю саму клетку (когда delta_row=0 и delta_column=0)
                if delta_row == 0 and delta_column == 0:
                    continue

                # Вычисляю координаты соседа
                new_row = row + delta_row
                new_col = col + delta_column

                # Проверяю, что сосед находится в пределах сетки
                if 0 <= new_row < self.cell_height and 0 <= new_col < self.cell_width:
                    # Добавляю значение клетки-соседа в список
                    neighbours.append(self.grid[new_row][new_col])

        return neighbours

    def get_next_generation(self) -> Grid:
        """
        Получить следующее поколение клеток.

        Returns
        ----------
        out : Grid
            Новое поколение клеток.
        """
        # Создаю новую пустую сетку того же размера
        new_grid = self.create_grid(randomize=False)

        # Прохожу по всем клеткам текущей сетки
        for row in range(self.cell_height):
            for col in range(self.cell_width):
                # Получаю соседей текущей клетки
                neighbours = self.get_neighbours((row, col))

                # Считаю количество живых соседей
                alive_neighbours = sum(neighbours)

                # Применяю правила игры "Жизнь"
                current_cell = self.grid[row][col]

                # Правило 1: Живая клетка с 2 или 3 соседями выживает
                if current_cell == 1:
                    if alive_neighbours == 2 or alive_neighbours == 3:
                        new_grid[row][col] = 1  # Клетка выживает
                    # Иначе клетка умирает (остается 0)

                # Правило 2: Мертвая клетка с ровно 3 соседями оживает
                else:
                    if alive_neighbours == 3:
                        new_grid[row][col] = 1  # Клетка рождается

        return new_grid
