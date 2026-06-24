from move_generator import MoveGenerator
from board_constants import BOARD_SIZE, SQUARE_SIZE


STARTING_POSITION = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
VALID_PIECES = set("KQRBNPkqrbnp")


class Board:
    def __init__(self, state=STARTING_POSITION):
        self.squares = self.parse_state(state)
        self.selected_square = None
        self.current_turn = "white"
        self.legal_moves = []
        self.move_generator = MoveGenerator(self)

    def parse_state(self, state):
        """Convert a FEN placement string into an 8x8 grid."""
        rows = state.split("/")
        if len(rows) != BOARD_SIZE:
            raise ValueError("Board state must contain exactly 8 rows.")

        squares = []
        for row_text in rows:
            row = []
            for symbol in row_text:
                if symbol in "12345678":
                    row.extend([None] * int(symbol))
                elif symbol in VALID_PIECES:
                    row.append(symbol)
                else:
                    raise ValueError(f"Invalid board symbol: {symbol!r}")

            if len(row) != BOARD_SIZE:
                raise ValueError(
                    f"Each board row must contain exactly 8 squares: {row_text!r}"
                )
            squares.append(row)

        return squares

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
            self.legal_moves = self.move_generator.get_pseudo_legal_moves(row, col)
        else:
            self.clear_selection()

    def clear_selection(self):
        self.selected_square = None
        self.legal_moves = []

    def handle_square_click(self, row, col):
        if not self.is_on_board(row, col):
            return

        clicked_piece = self.piece_at(row, col)

        if self.selected_square is None:
            if clicked_piece and self.is_current_turn_piece(clicked_piece):
                self.select_square(row, col)
            return

        if clicked_piece:
            if self.is_current_turn_piece(clicked_piece):
                self.select_square(row, col)
            else:
                self.clear_selection()
            return

        if (row, col) in self.legal_moves:
            self.move_piece(self.selected_square, (row, col))
            self.clear_selection()
            return

        self.clear_selection()

    def move_piece(self, start, end):
        start_row, start_col = start
        end_row, end_col = end

        piece = self.squares[start_row][start_col]
        self.squares[end_row][end_col] = piece
        self.squares[start_row][start_col] = None
        self.switch_turn()

    def piece_colour(self, piece):
        if piece is None:
            return None
        return "white" if piece.isupper() else "black"

    def is_current_turn_piece(self, piece):
        return self.piece_colour(piece) == self.current_turn

    def switch_turn(self):
        self.current_turn = "black" if self.current_turn == "white" else "white"
