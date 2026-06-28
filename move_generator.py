class MoveGenerator:
    def __init__(self, board):
        self.board = board

    def get_legal_move(self, row, col):
        legal_moves = []
        psuedo_moves = self.get_pseudo_legal_moves(row, col)

        for move in psuedo_moves:
            if not self.board.would_leave_king_in_check((row, col), move):
                legal_moves.append(move)

        return legal_moves

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
        piece = self.board.piece_at(row, col)
        direction = -1 if piece.isupper() else 1
        starting_row = 6 if piece.isupper() else 1
        moves = []

        one_step_row = row + direction
        if (
            self.board.is_on_board(one_step_row, col)
            and self.board.piece_at(one_step_row, col) is None
        ):
            moves.append((one_step_row, col))

            two_step_row = row + (2 * direction)
            if (
                row == starting_row
                and self.board.piece_at(two_step_row, col) is None
            ):
                moves.append((two_step_row, col))

        for col_offset in (-1, 1):
            target_row = row + direction
            target_col = col + col_offset
            if not self.board.is_on_board(target_row, target_col):
                continue

            target_piece = self.board.piece_at(target_row, target_col)
            if self.is_enemy_piece(piece, target_piece):
                moves.append((target_row, target_col))
            elif (
                target_piece is None
                and self.is_en_passant_move(row, col, target_col, piece)
            ):
                moves.append((target_row, target_col))

        return moves

    def get_knight_moves(self, row, col):
        piece = self.board.piece_at(row, col)
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

            target_piece = self.board.piece_at(target_row, target_col)
            if target_piece is None or self.is_enemy_piece(piece, target_piece):
                moves.append((target_row, target_col))

        return moves

    def get_bishop_moves(self, row, col):
        directions = [(-1, -1), (1, -1), (-1, 1), (1, 1)]
        moves = []
        for direct in directions:
            moves += self.get_sliding_moves(row, col, direct)
        return moves

    def get_rook_moves(self, row, col):
        directions = [(-1, 0), (1, 0), (0, 1), (0, -1)]
        moves = []
        for direct in directions:
            moves += self.get_sliding_moves(row, col, direct)
        return moves

    def get_queen_moves(self, row, col):
        moves = self.get_bishop_moves(row, col) + self.get_rook_moves(row, col)
        return moves

    def get_king_moves(self, row, col):
        directions = [(-1, -1), (0, -1), (1, -1), (1, 1), (-1, 1), (0, 1), (1, 0), (-1, 0)]
        piece = self.board.piece_at(row, col)
        moves = []
        for i, j in directions:
            target_row = row + i
            target_col = col + j
            if not self.board.is_on_board(target_row, target_col):
                continue

            target_piece = self.board.piece_at(target_row, target_col)
            if target_piece is None or self.is_enemy_piece(piece, target_piece):
                moves.append((row + i, col + j))
        return moves

    def get_sliding_moves(self, row, col, direction):
        moves = []
        row_offset, col_offset = direction
        moving_piece = self.board.piece_at(row, col)
        target_row = row + row_offset
        target_col = col + col_offset

        while self.board.is_on_board(target_row, target_col):
            target_piece = self.board.piece_at(target_row, target_col)
            if target_piece is None:
                moves.append((target_row, target_col))
            else:
                if self.is_enemy_piece(moving_piece, target_piece):
                    moves.append((target_row, target_col))
                break

            target_row += row_offset
            target_col += col_offset

        return moves

    def is_enemy_piece(self, moving_piece, target_piece):
        if moving_piece is None or target_piece is None:
            return False
        return self.board.piece_colour(moving_piece) != self.board.piece_colour(
            target_piece
        )

    def is_en_passant_move(self, row, col, target_col, piece):
        last_move = self.board.last_move
        if last_move is None:
            return False

        last_piece = last_move["piece"]
        start_row, start_col = last_move["start"]
        end_row, end_col = last_move["end"]

        return (
            last_piece.lower() == "p"
            and self.is_enemy_piece(piece, last_piece)
            and abs(end_row - start_row) == 2
            and end_row == row
            and end_col == target_col
            and abs(end_col - col) == 1
        )

    def get_attacked_squares(self, attacker):
        target = set()

        for i in range(8):
            for j in range(8):
                piece = self.board.piece_at(i, j)

                if self.board.piece_colour(piece) == attacker:
                    if piece.lower() == "p":
                        target.update(self.get_pawn_target(i, j, attacker))
                    else:
                        target.update(self.get_pseudo_legal_moves(i, j))
        return target

    def get_pawn_target(self, row, col, attacker):
        doa = 1 if attacker == "black" else -1
        target = []

        for i in [-1, 1]:
            temp_row = row + doa
            temp_col = col + i

            if self.board.is_on_board(temp_row, temp_col):
                target.append((temp_row, temp_col))

        return target
