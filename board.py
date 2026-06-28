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
        self.last_move = None
        self.game_status = "playing"
        self.winner = None
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
            self.legal_moves = self.move_generator.get_legal_move(row, col)
        else:
            self.clear_selection()

    def clear_selection(self):
        self.selected_square = None
        self.legal_moves = []

    def handle_square_click(self, row, col):
        if self.game_status in ("checkmate", "stalemate"):
            return

        if not self.is_on_board(row, col):
            return

        clicked_piece = self.piece_at(row, col)

        if self.selected_square is None:
            if clicked_piece and self.is_current_turn_piece(clicked_piece):
                self.select_square(row, col)
            return

        if (row, col) in self.legal_moves:
            self.move_piece(self.selected_square, (row, col))
            self.clear_selection()
            return

        if clicked_piece and self.is_current_turn_piece(clicked_piece):
            self.select_square(row, col)
            return

        self.clear_selection()

    def move_piece(self, start, end, evaluate_status=True):
        start_row, start_col = start
        end_row, end_col = end

        piece = self.squares[start_row][start_col]
        captured_piece = self.squares[end_row][end_col]

        # An en passant capture lands diagonally on an empty square.
        if (
            piece.lower() == "p"
            and start_col != end_col
            and captured_piece is None
        ):
            captured_piece = self.squares[start_row][end_col]
            self.squares[start_row][end_col] = None

        self.squares[end_row][end_col] = piece
        self.squares[start_row][start_col] = None

        if piece == "P" and end_row == 0:
            self.squares[end_row][end_col] = "Q"
        elif piece == "p" and end_row == BOARD_SIZE - 1:
            self.squares[end_row][end_col] = "q"

        self.last_move = {
            "start": start,
            "end": end,
            "piece": piece,
            "captured_piece": captured_piece,
        }
        self.switch_turn()

        if evaluate_status:
            self.game_status = self.get_game_status()
            if self.game_status == "checkmate":
                self.winner = (
                    "black" if self.current_turn == "white" else "white"
                )
            elif self.game_status == "stalemate":
                self.winner = None

    def piece_colour(self, piece):
        if piece is None:
            return None
        return "white" if piece.isupper() else "black"

    def is_current_turn_piece(self, piece):
        return self.piece_colour(piece) == self.current_turn

    def switch_turn(self):
        self.current_turn = "black" if self.current_turn == "white" else "white"

    def find_king(self, side):
        king = "K" if side == "white" else "k"

        return next(
            ((i, j) for i in range(8) for j in range(8)
             if self.piece_at(i, j) == king),
             None
        )

    def is_in_check(self, colour):
        attacker = "white" if colour == "black" else "black"
        attacked_squares = self.move_generator.get_attacked_squares(attacker)
        king_pos = self.find_king(colour)

        return king_pos in attacked_squares

    def would_leave_king_in_check(self, start, end):
        colour = self.piece_colour(self.piece_at(*start))
        save_square = [row[:] for row in self.squares]
        save_turn = self.current_turn
        save_move = self.last_move

        try:
            self.move_piece(start, end, evaluate_status=False)
            return self.is_in_check(colour)
        finally:
            self.squares = save_square
            self.current_turn = save_turn
            self.last_move = save_move

    def get_game_status(self):
        colour = self.current_turn
        has_move = self.has_legal_moves(colour)

        if self.is_in_check(colour):
            if has_move:
                return "check"
            else:
                return "checkmate"

        return "playing" if has_move else "stalemate"

    def has_legal_moves(self, colour):
        for i in range(8):
            for j in range(8):
                piece = self.piece_at(i, j)

                if (
                    self.piece_colour(piece) == colour
                    and self.move_generator.get_legal_move(i, j)
                ):
                    return True

        return False
