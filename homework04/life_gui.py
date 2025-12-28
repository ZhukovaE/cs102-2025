import pygame
from life import GameOfLife

# from pygame.locals import *
from ui import UI


class GUI(UI):
    def __init__(self, life: GameOfLife, cell_size: int = 10, speed: int = 10) -> None:
        super().__init__(life)

        self.cell_size = cell_size
        self.speed = speed

        # Вычисляем размер окна
        self.width = life.cols * cell_size
        self.height = life.rows * cell_size

        # Инициализация pygame
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Game of Life")

    def draw_lines(self) -> None:
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(
                self.screen, pygame.Color("black"), (x, 0), (x, self.height)
            )
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(
                self.screen, pygame.Color("black"), (0, y), (self.width, y)
            )
        pass

    def draw_grid(self) -> None:
        for row in range(self.life.rows):
            for col in range(self.life.cols):
                if self.life.curr_generation[row][col] == 1:
                    color = pygame.Color("green")
                else:
                    color = pygame.Color("white")

                x = col * self.cell_size
                y = row * self.cell_size

                rect = pygame.Rect(x, y, self.cell_size, self.cell_size)
                pygame.draw.rect(self.screen, color, rect)

    def run(self) -> None:
        clock = pygame.time.Clock()
        paused = False  # Флаг для паузы

        running = True
        while (
            running
            and self.life.is_changing
            and not self.life.is_max_generations_exceeded
        ):

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:  # Пробел - пауза/продолжение
                        paused = not paused
                    elif event.key == pygame.K_q:  # Q - выход
                        running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and paused:  # Клики при паузе
                    x, y = pygame.mouse.get_pos()
                    col = x // self.cell_size
                    row = y // self.cell_size
                    if 0 <= row < self.life.rows and 0 <= col < self.life.cols:
                        # Инвертирую состояние клетки
                        self.life.curr_generation[row][col] = (
                            1 - self.life.curr_generation[row][col]
                        )

            # Очищаю экран
            self.screen.fill(pygame.Color("white"))

            # Рисую клетки
            self.draw_grid()

            # Рисую сетку
            self.draw_lines()

            # Отображаю статус паузы
            if paused:
                font = pygame.font.SysFont(None, 36)
                text = font.render(
                    "PAUSED (SPACE to resume)", True, pygame.Color("red")
                )
                self.screen.blit(text, (10, 10))
                hint = font.render("Click cells to toggle", True, pygame.Color("blue"))
                self.screen.blit(hint, (10, 50))
            else:
                # Выполняю шаг игры только если не на паузе
                self.life.step()

            pygame.display.flip()
            clock.tick(self.speed)

        pygame.quit()
