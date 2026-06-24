import pygame

from board import Board
from board_constants import HEIGHT, WIDTH
from renderer import BoardRenderer


FPS = 60
WINDOW_TITLE = "Chess"


def handle_events(board):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            row, col = board.get_square_from_mouse(event.pos)
            board.handle_square_click(row, col)
    return True


def draw_frame(screen, board, renderer):
    renderer.draw(screen, board)
    pygame.display.flip()


def main():
    pygame.init()
    pygame.display.set_caption(WINDOW_TITLE)

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    board = Board()
    renderer = BoardRenderer()
    running = True

    try:
        while running:
            clock.tick(FPS)
            running = handle_events(board)
            draw_frame(screen, board, renderer)
    finally:
        pygame.quit()


if __name__ == "__main__":
    main()
