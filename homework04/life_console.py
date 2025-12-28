import curses

from life import GameOfLife
from ui import UI


class Console(UI):
    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

    def draw_borders(self, screen) -> None:
        """Отобразить рамку."""
        screen.border()

    def draw_grid(self, screen) -> None:
        """Отобразить состояние клеток."""
        # Очищаю экран
        screen.clear()

        # Рисую рамку
        self.draw_borders(screen)

        # Информация внутри рамки
        screen.addstr(1, 2, f"Generation: {self.life.generations}")
        screen.addstr(2, 2, "Press 'q' to quit")

        # Рисую клетки внутри рамки (начиная с 4 строки)
        for i in range(self.life.rows):
            for j in range(self.life.cols):
                if self.life.curr_generation[i][j] == 1:
                    try:
                        # +4 чтобы было под информацией, +1 из-за левой рамки
                        screen.addch(i + 4, j + 1, "#")
                    except curses.error:
                        pass  # Если не помещается
                else:
                    try:
                        screen.addch(i + 4, j + 1, " ")
                    except curses.error:
                        pass

    def run(self) -> None:
        screen = curses.initscr()
        try:
            # Настройки
            curses.curs_set(0)  # Скрыть курсор
            screen.nodelay(True)  # Неблокирующий ввод

            # Игровой цикл
            while self.life.is_changing and not self.life.is_max_generations_exceeded:

                # Рисую игру
                self.draw_grid(screen)
                screen.refresh()

                # Проверяю нажатие 'q'
                if screen.getch() == ord("q"):
                    break

                # Делаю шаг игры
                self.life.step()

                # Задержка
                curses.napms(200)

        finally:
            # Восстанавливаю терминал
            curses.endwin()
        curses.endwin()
