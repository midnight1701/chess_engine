class GameState:
    def __init__(self):
        # Game state
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
        ]

        self.move = {"p": self.get_pawn_moves, "R": self.get_rook_moves, "N": self.get_knight_moves,
                     "B": self.get_bishop_moves, "Q": self.get_queen_moves, "K": self.get_king_moves}
        self.white_to_move = True
        self.move_log = []

    def get_all_moves(self):
        moves = []
        for r in range(len(self.board)):
            for f in range(len(self.board[r])):
                turn = self.board[r][f][0]
                if (turn == "w" and self.white_to_move) or (turn == "b" and not self.white_to_move):
                    piece = self.board[r][f][1]
                    self.move[piece](r, f, moves)
        return moves

    def get_valid_moves(self):
        return self.get_all_moves()

    def get_pawn_moves(self, r, f, moves):
        if self.white_to_move:
            if self.board[r - 1][f] == "--":
                moves.append(Move([(r, f), (r - 1, f)], self.board))
                if self.board[r - 2][f] == "--" and r == 6:
                    moves.append(Move([(r, f), (r - 2, f)], self.board))

            if f < 7:
                if self.board[r - 1][f + 1][0] == "b":
                    moves.append(Move([(r, f), (r - 1, f + 1)], self.board))

            if f > 0:
                if self.board[r - 1][f - 1][0] == "b":
                    moves.append(Move([(r, f), (r - 1, f - 1)], self.board))


        else:
            if self.board[r + 1][f] == "--":
                moves.append(Move([(r, f), (r + 1, f)], self.board))
                if self.board[r + 2][f] == "--" and r == 1:
                    moves.append(Move([(r, f), (r + 2, f)], self.board))

            if f < 7:
                if self.board[r + 1][f + 1][0] == "w":
                    moves.append(Move([(r, f), (r + 1, f + 1)], self.board))

            if f > 0:
                if self.board[r + 1][f - 1][0] == "w":
                    moves.append(Move([(r, f), (r + 1, f - 1)], self.board))


    def get_rook_moves(self, r, f, moves):
        direction = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        enemy_color = "b" if self.white_to_move else "w"
        for d in direction:
            for i in range(1, 8):
                end_r = r + d[0] * i
                end_f = f + d[1] * i
                if 0 <= end_r < 8 and 0 <= end_f < 8:
                    piece = self.board[end_r][end_f]
                    if piece == "--":
                        moves.append(Move([(r, f), (end_r, end_f)], self.board))
                    elif piece[0] == enemy_color:
                        moves.append(Move([(r, f), (end_r, end_f)], self.board))
                        break
                    else:
                        break

                else:
                    break


    def get_knight_moves(self, r, f, moves):
        direction = [(2, 1), (2, -1), (-2, -1), (-2, 1), (1, 2), (1, -2), (-1, 2), (-1, -2)]
        ally_color = "w" if self.white_to_move else "b"
        for d in direction:
            end_r = r + d[0]
            end_f = f + d[1]
            if 0 <= end_r < 8 and 0 <= end_f < 8:
                piece = self.board[end_r][end_f]
                if piece[0] != ally_color:
                    moves.append(Move([(r, f), (end_r, end_f)], self.board))


    def get_bishop_moves(self, r, f, moves):
        direction = [(1, 1), (1, -1), (-1, -1), (-1, 1)]
        enemy_color = "b" if self.white_to_move else "w"
        for d in direction:
            for i in range(1, 8):
                end_r = r + d[0] * i
                end_f = f + d[1] * i
                if 0 <= end_r < 8 and 0 <= end_f < 8:
                    piece = self.board[end_r][end_f]
                    if piece == "--":
                        moves.append(Move([(r, f), (end_r, end_f)], self.board))
                    elif piece[0] == enemy_color:
                        moves.append(Move([(r, f), (end_r, end_f)], self.board))
                        break
                    else:
                        break

                else:
                    break


    def get_queen_moves(self, r, f, moves):
        self.get_rook_moves(r, f, moves)
        self.get_bishop_moves(r, f, moves)

    def get_king_moves(self, r, f, moves):
        direction = [(1, 1), (1, -1), (1, 0), (0, 1), (0, -1), (-1, 0), (-1, -1), (-1, 1)]
        ally_color = "w" if self.white_to_move else "b"
        for d in direction:
            end_r = r + d[0]
            end_f = f + d[1]
            if 0 <= end_r < 8 and 0 <= end_f < 8:
                piece = self.board[end_r][end_f]
                if piece[0] != ally_color:
                    moves.append(Move([(r, f), (end_r, end_f)], self.board))

    def make_move(self, move):
        self.board[move.start_r][move.start_f] = "--"
        self.board[move.end_r][move.end_f] = move.moved_piece
        self.white_to_move = not self.white_to_move
        self.move_log.append(move)

    def undo_move(self):
        if len(self.move_log) != 0:
            move = self.move_log.pop()
            self.board[move.start_r][move.start_f] = move.moved_piece
            self.board[move.end_r][move.end_f] = move.end_piece
            self.white_to_move = not self.white_to_move

class Move:
    rank = {0: "8", 1: "7", 2: "6", 3: "5", 4: "4", 5: "3", 6: "2", 7: "1"}
    file = {0: "a", 1: "b", 2: "c", 3: "d", 4: "e", 5: "f", 6: "g", 7: "h"}
    piece_to_piece = {"wR": "R", "wN": "N", "wB": "B", "wQ": "Q", "wK": "K", "wp": "",
                      "bR": "R", "bN": "N", "bB": "B", "bQ": "Q", "bK": "K", "bp": ""}

    def __init__(self, click_lst, game_board):
        self.start_sq = click_lst[0]
        self.end_sq = click_lst[1]
        self.start_r = self.start_sq[0]
        self.start_f = self.start_sq[1]
        self.end_r = self.end_sq[0]
        self.end_f = self.end_sq[1]
        self.moved_piece = game_board[self.start_r][self.start_f]
        self.end_piece = game_board[self.end_r][self.end_f]
        self.moveID = self.start_r * 1000 + self.start_f * 100 + self.end_r * 10 + self.end_f

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False


    def get_move_notation(self):
        coor = self.piece_to_piece[self.moved_piece] + self.file[self.end_f] + self.rank[self.end_r]
        return coor
