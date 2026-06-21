import pygame
from board import Board, WIDTH, HEIGHT

pygame.init()
fps = 60
pygame.display.set_caption("Chess")
screen = pygame.display.set_mode([WIDTH, HEIGHT])
timer = pygame.time.Clock()

board = Board()


running = True

while running:
    timer.tick(fps)
    screen.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    board.draw(screen)
    pygame.display.update()

pygame.quit()


