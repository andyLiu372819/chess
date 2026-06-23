from pathlib import Path

import pygame


WIDTH = 900
HEIGHT = 900
BOARD_SIZE = 8
SQUARE_SIZE = WIDTH // BOARD_SIZE
ASSET_DIR = Path(__file__).resolve().parent / "assets"
STARTING_POSITION = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"

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
    def __init__(self, state=STARTING_POSITION):
        self.font = pygame.font.SysFont("Arial", 50)
        self.squares = self.parse_state(state)
        self.board_sprite = self.load_board_sprite()
        self.piece_sprites = self.load_piece_sprites()
        self.selected_square = None
        self.current_turn = "white"

    def parse_state(self, state):
        """Convert a FEN placement string into an 8x8 grid.

        The renderer wants direct row/column access, and the future move logic
        will too. Keeping this conversion here means the rest of the class never
        has to count through the compact FEN string while drawing or moving.
        """
        rows = state.split("/")
        if len(rows) != BOARD_SIZE:
            raise ValueError("Board state must contain exactly 8 rows.")

        squares = []
        for row_text in rows:
            row = []
            for symbol in row_text:
                if symbol in "12345678":
                    row.extend([None] * int(symbol))
                elif symbol in PIECE_SPRITES:
                    row.append(symbol)
                else:
                    raise ValueError(f"Invalid board symbol: {symbol!r}")

            if len(row) != BOARD_SIZE:
                raise ValueError(
                    f"Each board row must contain exactly 8 squares: {row_text!r}"
                )
            squares.append(row)

        return squares

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
        
        self.draw_selected_square(screen)

        for row_index, row in enumerate(self.squares):
            for col_index, piece in enumerate(row):
                if piece:
                    self.draw_piece(screen, piece, row_index, col_index)

    def get_square_from_mouse(self, position):
        x, y = position
        return y // SQUARE_SIZE, x // SQUARE_SIZE

    def is_on_board(self, row, col):
        return 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE

    def piece_at(self, row, col):
        if not self.is_on_board(row, col):
            return None
        return self.squares[row][col]
    
    def select_square(self, row, col):
        if self.piece_at(row, col):
            self.selected_square = (row, col)
        else:
            self.selected_square = None
    
    def draw_selected_square(self, screen):
        if not self.selected_square:
            return

        row, col = self.selected_square
        rect = pygame.Rect(
            col * SQUARE_SIZE,
            row * SQUARE_SIZE,
            SQUARE_SIZE,
            SQUARE_SIZE,
        )
        pygame.draw.rect(screen, (255, 220, 90), rect, 5)
    
    def handle_square_click(self, row, col):
        if not self.is_on_board(row, col):
            return
        
        if self.selected_square is None:
            if self.piece_at(row, col):
                if self.is_current_turn_piece(self.piece_at(row, col)):
                    self.selected_square = (row, col)
            return
        
        if self.piece_at(row, col):
            if self.is_current_turn_piece(self.piece_at(row, col)):
                    self.selected_square = (row, col)
            return

        self.move_piece(self.selected_square, (row, col))
        self.selected_square = None

    def move_piece(self, start, end):
        start_row, start_col = start
        end_row, end_col = end

        piece = self.squares[start_row][start_col]
        self.squares[end_row][end_col] = piece
        self.squares[start_row][start_col] = None

        self.switch_turn()

    def piece_colour(self, piece):
        if piece is None:
            return
        return "white" if piece.isupper() else "black"
    
    def is_current_turn_piece(self, piece):
        return self.piece_colour(piece) == self.current_turn
    
    def switch_turn(self):
        self.current_turn = "black" if self.current_turn == "white" else "white"
    

