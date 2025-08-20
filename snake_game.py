import curses
import random

# Constants for game dimensions
WIDTH = 40
HEIGHT = 20


def create_food(snake):
    """Generate food coordinates not occupied by the snake."""
    while True:
        food = [random.randint(1, HEIGHT - 2), random.randint(1, WIDTH - 2)]
        if food not in snake:
            return food


def main(stdscr):
    # Initialize window
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.keypad(1)
    stdscr.timeout(100)

    # Initial snake position (center)
    snake = [[HEIGHT // 2, WIDTH // 2 + i] for i in range(3)]
    direction = curses.KEY_LEFT
    food = create_food(snake)
    score = 0

    while True:
        stdscr.clear()

        # Draw borders
        for x in range(WIDTH):
            stdscr.addstr(0, x, '#')
            stdscr.addstr(HEIGHT - 1, x, '#')
        for y in range(HEIGHT):
            stdscr.addstr(y, 0, '#')
            stdscr.addstr(y, WIDTH - 1, '#')

        # Draw snake and food
        for y, x in snake:
            stdscr.addstr(y, x, '*')
        stdscr.addstr(food[0], food[1], 'O')
        stdscr.addstr(0, 2, f'Score: {score}')

        stdscr.refresh()

        # Handle input
        key = stdscr.getch()
        if key in [curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT]:
            opposite = {curses.KEY_UP: curses.KEY_DOWN,
                        curses.KEY_DOWN: curses.KEY_UP,
                        curses.KEY_LEFT: curses.KEY_RIGHT,
                        curses.KEY_RIGHT: curses.KEY_LEFT}
            if key != opposite.get(direction):
                direction = key

        # Move snake
        head = snake[0][:]
        if direction == curses.KEY_UP:
            head[0] -= 1
        elif direction == curses.KEY_DOWN:
            head[0] += 1
        elif direction == curses.KEY_LEFT:
            head[1] -= 1
        elif direction == curses.KEY_RIGHT:
            head[1] += 1

        snake.insert(0, head)

        # Check for collision with borders or self
        if (head[0] in [0, HEIGHT - 1] or
                head[1] in [0, WIDTH - 1] or
                head in snake[1:]):
            msg = f"Game Over! Score: {score}. Press any key to exit."
            stdscr.nodelay(0)
            stdscr.addstr(HEIGHT // 2, WIDTH // 2 - len(msg) // 2, msg)
            stdscr.getch()
            break

        # Check if food eaten
        if head == food:
            food = create_food(snake)
            score += 1
        else:
            snake.pop()


if __name__ == "__main__":
    curses.wrapper(main)
