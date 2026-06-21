import pygame


WIDTH = 900
HEIGHT = 900
LS = 0
TS = 0

class Board():

    def __init__(self, state='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR'):
        self.state = state
        self.font = pygame.font.SysFont('Ariel', 50)

    def draw(self, screen: pygame.Surface):
        left, top = LS, TS
        white = True
        for i in self.state:
            if i.isnumeric():
                for j in range(int(i)):
                    rect = pygame.Rect(left, top, WIDTH / 8, HEIGHT / 8)
                    if white:
                        pygame.draw.rect(screen, (255, 255, 255), rect)
                    else:
                        pygame.draw.rect(screen, (192, 192, 192), rect)
                    white = not white
                    left += WIDTH/8
            elif i.isalpha():
                rect = pygame.Rect(left, top, WIDTH / 8, HEIGHT / 8)
                center = ((left + left + WIDTH/8)/2, (top + top + HEIGHT/8)/2)
                if white:
                    pygame.draw.rect(screen, (255, 255, 255), rect)
                else:
                    pygame.draw.rect(screen, (192, 192, 192), rect)
                screen.blit(self.font.render(i, True, (0, 0, 0)), center)
                left += WIDTH/8
                white = not white
            else:
                left = LS
                top += HEIGHT/8
                white = not white


