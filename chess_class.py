import chess
import numpy as np


class ChessBoard:
    def __init__(self):
        self.row_count = 8
        self.column_count = 8
        self.action_count = self.row_count * self.column_count

    def display_board(self, state):
        print(state)

    def get_value_terminal_state(self, state):
        if state.is_game_over() and (state.result() == "1-0" or state.result() == "0-1"):
            return 1, True
        elif state.is_game_over():
            return 0, True
        return 0, False

    def get_initial_state(self):
        return chess.Board()

    def get_next_state(self, state, action):
        try:
            move = chess.Move.from_uci(action)
            if move in state.legal_moves:
                state.push(move)
                return state
            else:
                print("Illegal move.")
                return False
        except ValueError:
            print("Invalid UCI format.")
            return False

    def board_to_array(self, state, flip=False):
        # Create a dictionary to map pieces to integers
        piece_to_int = {
            'P': 1, 'N': 2, 'B': 3, 'R': 4, 'Q': 5, 'K': 6,
            'p': 7, 'n': 8, 'b': 9, 'r': 10, 'q': 11, 'k': 12
        }
        # Create an 8x8 numpy array filled with 0
        board_array = np.zeros((8, 8), dtype=int)

        for square in range(0, 64):
            piece = state.piece_at(square)
            if piece:
                board_array[chess.square_rank(square), chess.square_file(square)] = piece_to_int[piece.symbol()]
        if not flip:
            return np.flip(board_array, axis=0)
        return board_array
    def load_position_from_fen(self, fen_str):
        try:
            board = chess.Board(fen_str)
            return board
        except ValueError as e:
            print(f"Error loading FEN: {e}")
        return

    def get_legal_moves(self, board):
        return [move.uci() for move in board.legal_moves]


# Example usage
game = ChessBoard()


fen_str = "r1bk3r/p2pBpNp/n4n2/1p1NP2P/6P1/3P4/P1P1K3/q5b1 b KQkq - 0 4"
# Simulate some moves
state = game.load_position_from_fen(fen_str)
print(chess.WHITE)
print(state.legal_moves)
print(game.get_value_terminal_state(state))
