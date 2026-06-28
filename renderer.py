import pygame

from board_constants import ASSET_DIR, BOARD_SIZE, HEIGHT, SQUARE_SIZE, WIDTH


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


class BoardRenderer:
    def __init__(self):
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

    def draw(self, screen, board):
        self.draw_board(screen)
        self.draw_selected_square(screen, board)
        self.draw_pieces(screen, board)
        self.draw_legal_moves(screen, board)

    def draw_board(self, screen):
        if self.board_sprite:
            screen.blit(self.board_sprite, (0, 0))
        else:
            self.draw_fallback_board(screen)

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

    def draw_selected_square(self, screen, board):
        if not board.selected_square:
            return

        row, col = board.selected_square
        rect = pygame.Rect(
            col * SQUARE_SIZE,
            row * SQUARE_SIZE,
            SQUARE_SIZE,
            SQUARE_SIZE,
        )
        pygame.draw.rect(screen, (255, 220, 90), rect, 5)

    def draw_legal_moves(self, screen, board):
        for row, col in board.legal_moves:
            center = (
                col * SQUARE_SIZE + SQUARE_SIZE // 2,
                row * SQUARE_SIZE + SQUARE_SIZE // 2,
            )
            if board.piece_at(row, col):
                radius = SQUARE_SIZE // 2 - 8
                pygame.draw.circle(screen, (200, 70, 70), center, radius, 5)
            else:
                pygame.draw.circle(screen, (80, 180, 100), center, 12)

    def draw_pieces(self, screen, board):
        for row_index, row in enumerate(board.squares):
            for col_index, piece in enumerate(row):
                if piece:
                    self.draw_piece(screen, piece, row_index, col_index)

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
