class MoveGenerator:
    def __init__(self, board):
        self.board = board

    def get_pseudo_legal_moves(self, row, col):
        piece = self.board.piece_at(row, col)
        if piece is None:
            return []

        piece_type = piece.lower()
        if piece_type == "p":
            return self.get_pawn_moves(row, col)
        if piece_type == "n":
            return self.get_knight_moves(row, col)
        if piece_type == "b":
            return self.get_bishop_moves(row, col)
        if piece_type == "r":
            return self.get_rook_moves(row, col)
        if piece_type == "q":
            return self.get_queen_moves(row, col)
        if piece_type == "k":
            return self.get_king_moves(row, col)

        return []

    def get_pawn_moves(self, row, col):
        return []

    def get_knight_moves(self, row, col):
        offsets = [
            (-2, -1),
            (-2, 1),
            (-1, -2),
            (-1, 2),
            (1, -2),
            (1, 2),
            (2, -1),
            (2, 1),
        ]

        moves = []
        for row_offset, col_offset in offsets:
            target_row = row + row_offset
            target_col = col + col_offset

            if not self.board.is_on_board(target_row, target_col):
                continue

            if self.board.piece_at(target_row, target_col) is None:
                moves.append((target_row, target_col))

        return moves

    def get_bishop_moves(self, row, col):
        return []

    def get_rook_moves(self, row, col):
        return []

    def get_queen_moves(self, row, col):
        return []

    def get_king_moves(self, row, col):
        return []

    def get_sliding_moves(self, row, col, directions):
        return []
