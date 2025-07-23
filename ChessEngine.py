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

        self.move_function = {"p": self.get_pawn_moves, "R": self.get_rook_moves, "N": self.get_knight_moves,
                              "B": self.get_bishop_moves, "Q": self.get_queen_moves, "K": self.get_king_moves}
        self.white_to_move = True
        self.move_log = []
        self.white_king_coor = (7, 4)
        self.black_king_coor = (0, 4)

        self.checkmate = False
        self.stalemate = False

    # Make a move
    def make_move(self, move):
        self.board[move.start_r][move.start_f] = "--"
        self.board[move.end_r][move.end_f] = move.moved_piece
        self.move_log.append(move)
        self.white_to_move = not self.white_to_move

        if move.moved_piece == "wK":
            self.white_king_coor = (move.end_r, move.end_f)
        elif move.moved_piece == "bK":
            self.black_king_coor = (move.end_r, move.end_f)


    # Undo the latest move
    def undo_move(self):
        if len(self.move_log) == 0:
            print("Cannot undo when no move has been made")
            return
        move = self.move_log.pop()
        self.board[move.start_r][move.start_f] = move.moved_piece
        self.board[move.end_r][move.end_f] = move.end_piece
        self.white_to_move = not self.white_to_move

        if move.moved_piece == "wK":
            self.white_king_coor = (move.start_r, move.start_f)
        elif move.moved_piece == "bK":
            self.black_king_coor = (move.start_r, move.start_f)


    # Get a list of all moves (valid)
    def get_valid_moves(self):
        moves = self.get_all_moves()
        for i in range(len(moves) - 1, -1, -1):
            self.make_move(moves[i])
            self.white_to_move = not self.white_to_move
            if self.get_enemy_check():
                moves.remove(moves[i])
            self.white_to_move = not self.white_to_move
            self.undo_move()

        if len(moves) == 0:
            if self.get_enemy_check():
                self.checkmate = True
                print(("White" if not self.white_to_move else "Black") + " " + "win by checkmate")
            else:
                self.stalemate = True
                print("Draw by stalemate")
        else:
            self.checkmate = False
            self.stalemate = False

        return moves


    # Get all possible moves (Valid & Invalid)
    def get_all_moves(self):
        moves = []
        for r in range(len(self.board)):
            for f in range(len(self.board[r])):
                turn = self.board[r][f][0]
                piece = self.board[r][f][1]
                if (turn == "w" and self.white_to_move) or (turn == "b" and not self.white_to_move):
                    if piece != "--":
                        self.move_function[piece](r, f, moves)
        return moves


    # Return True if the king is in check, False if otherwise
    def get_enemy_check(self):
        if self.white_to_move:
            return self.enemy_attack(self.white_king_coor[0], self.white_king_coor[1])
        else:
            return self.enemy_attack(self.black_king_coor[0], self.black_king_coor[1])


    # Check if the king is under attack
    def enemy_attack(self, r, f):
        self.white_to_move = not self.white_to_move
        opponent_moves = self.get_all_moves()
        self.white_to_move = not self.white_to_move
        for m in opponent_moves:
            if m.end_r == r and m.end_f == f:
                return True
        return False


    def get_pawn_moves(self, r, f, moves):
        if self.white_to_move:
            if self.board[r - 1][f] == "--":
                moves.append(Move((r, f), (r - 1, f), self.board))
                if self.board[r - 2][f] == "--" and r == 6:
                    moves.append(Move((r, f), (r - 2, f), self.board))

            if f < 7 and self.board[r - 1][f + 1][0] == "b":
                moves.append(Move((r, f), (r - 1, f + 1), self.board))

            if f > 0 and self.board[r - 1][f - 1][0] == "b":
                moves.append(Move((r, f), (r - 1, f - 1), self.board))


        if not self.white_to_move:
            if self.board[r + 1][f] == "--":
                moves.append(Move((r, f), (r + 1, f), self.board))
                if self.board[r + 2][f] == "--" and r == 1:
                    moves.append(Move((r, f), (r + 2, f), self.board))

            if f < 7 and self.board[r + 1][f + 1][0] == "w":
                moves.append(Move((r, f), (r + 1, f + 1), self.board))

            if f > 0 and self.board[r + 1][f - 1][0] == "w":
                moves.append(Move((r, f), (r + 1, f - 1), self.board))


    def get_rook_moves(self, r, f, moves):
        direction = ((1, 0), (-1, 0), (0, 1), (0, -1))
        enemy_color = "b" if self.white_to_move else "w"
        for d in direction:
            for i in range(1, 8):
                end_r = r + (d[0] * i)
                end_f = f + (d[1] * i)
                if 0 <= end_r < len(self.board) and 0 <= end_f < len(self.board[end_r]):
                    piece = self.board[end_r][end_f]
                    if piece == "--":
                        moves.append(Move((r, f), (end_r, end_f), self.board))
                    elif piece[0] == enemy_color:
                        moves.append(Move((r, f), (end_r, end_f), self.board))
                        break
                    else:
                        break

                else:
                    break


    def get_knight_moves(self, r, f, moves):
        direction = ((2, 1), (2, -1), (-2, -1), (-2, 1), (1, 2), (1, -2), (-1, 2), (-1, -2))
        ally_color = "w" if self.white_to_move else "b"
        for d in direction:
            end_r = r + d[0]
            end_f = f + d[1]
            if 0 <= end_r < len(self.board) and 0 <= end_f < len(self.board[end_r]):
                piece = self.board[end_r][end_f]
                if piece[0] != ally_color:
                    moves.append(Move((r, f), (end_r, end_f), self.board))


    def get_bishop_moves(self, r, f, moves):
        direction = ((1, 1), (1, -1), (-1, -1), (-1, 1))
        enemy_color = "b" if self.white_to_move else "w"
        for d in direction:
            for i in range(1, 8):
                end_r = r + (d[0] * i)
                end_f = f + (d[1] * i)
                if 0 <= end_r < len(self.board) and 0 <= end_f < len(self.board[end_r]):
                    piece = self.board[end_r][end_f]
                    if piece == "--":
                        moves.append(Move((r, f), (end_r, end_f), self.board))
                    elif piece[0] == enemy_color:
                        moves.append(Move((r, f), (end_r, end_f), self.board))
                        break
                    else:
                        break

                else:
                    break


    def get_queen_moves(self, r, f, moves):
        self.get_rook_moves(r, f, moves)
        self.get_bishop_moves(r, f, moves)


    def get_king_moves(self, r, f, moves):
        direction = ((1, 1), (1, -1), (1, 0), (0, 1), (0, -1), (-1, 0), (-1, -1), (-1, 1))
        ally_color = "w" if self.white_to_move else "b"
        for d in direction:
            end_r = r + d[0]
            end_f = f + d[1]
            if 0 <= end_r < len(self.board) and 0 <= end_f < len(self.board[end_r]):
                piece = self.board[end_r][end_f]
                if piece[0] != ally_color:
                    moves.append(Move((r, f), (end_r, end_f), self.board))


# Data of a chess move
class Move:
    def __init__(self, start_sq, end_sq, game_board):
        self.start_r = start_sq[0]
        self.start_f = start_sq[1]
        self.end_r = end_sq[0]
        self.end_f = end_sq[1]
        self.moved_piece = game_board[self.start_r][self.start_f]
        self.end_piece = game_board[self.end_r][self.end_f]
        self.moveID = self.start_r * 1000 + self.start_f * 100 + self.end_r * 10 + self.end_f


    def __eq__(self, other):
        return isinstance(other, Move) and self.moveID == other.moveID
