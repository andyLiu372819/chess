from pathlib import Path

import pygame


WIDTH = 900
HEIGHT = 900
BOARD_SIZE = 8
SQUARE_SIZE = WIDTH // BOARD_SIZE
ASSET_DIR = Path(__file__).resolve().parent / "assets"

PIECE_SPRITES = {
    "K": "white_king.png",
    "Q": "white_queen.png",
    "R": "white_rook.png",
    "B": "white_bishop.png",
    "N": "white_knight.png",
    "P": "white_pawn.png",
    "k": "black_king.png",
    "q": "black_queen.png",
    "r": "black_rook.png",
    "b": "black_bishop.png",
    "n": "black_knight.png",
    "p": "black_pawn.png",
}


class Board:
    def __init__(self, state="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"):
        self.state = state
        self.font = pygame.font.SysFont("Arial", 50)
        self.board_sprite = self.load_board_sprite()
        self.piece_sprites = self.load_piece_sprites()

    def load_board_sprite(self):
        board_path = ASSET_DIR / "board.png"
        if not board_path.exists():
            return None

        sprite = pygame.image.load(str(board_path)).convert()
        return pygame.transform.scale(sprite, (WIDTH, HEIGHT))

    def load_piece_sprites(self):
        sprites = {}
        for symbol, filename in PIECE_SPRITES.items():
            path = ASSET_DIR / "pieces" / filename
            if path.exists():
                sprite = pygame.image.load(str(path)).convert_alpha()
                sprites[symbol] = pygame.transform.smoothscale(
                    sprite,
                    (SQUARE_SIZE, SQUARE_SIZE),
                )
        return sprites

    def draw_fallback_board(self, screen):
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                color = (238, 238, 210) if (row + col) % 2 == 0 else (118, 150, 86)
                rect = pygame.Rect(
                    col * SQUARE_SIZE,
                    row * SQUARE_SIZE,
                    SQUARE_SIZE,
                    SQUARE_SIZE,
                )
                pygame.draw.rect(screen, color, rect)

    def draw_piece(self, screen, symbol, row, col):
        x = col * SQUARE_SIZE
        y = row * SQUARE_SIZE
        sprite = self.piece_sprites.get(symbol)

        if sprite:
            screen.blit(sprite, (x, y))
            return

        text = self.font.render(symbol, True, (20, 20, 20))
        rect = text.get_rect(center=(x + SQUARE_SIZE / 2, y + SQUARE_SIZE / 2))
        screen.blit(text, rect)

    def draw(self, screen):
        if self.board_sprite:
            screen.blit(self.board_sprite, (0, 0))
        else:
            self.draw_fallback_board(screen)

        row = 0
        col = 0
        for symbol in self.state:
            if symbol == "/":
                row += 1
                col = 0
            elif symbol.isnumeric():
                col += int(symbol)
            elif symbol.isalpha():
                self.draw_piece(screen, symbol, row, col)
                col += 1
