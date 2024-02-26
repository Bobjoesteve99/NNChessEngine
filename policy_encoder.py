import chess
import numpy as np

move_length = np.arange(1, 8)

bishop_move_vec = np.array([
    [1, 1] * move_length,  # NE
    [1, -1] * move_length,  # NW
    [-1, 1] * move_length,  # SE
    [-1, -1] * move_length,  # SW
])

rook_move_vec = np.array([
    [0, 1] * move_length,  # N
    [1, 0] * move_length,  # E
    [0, -1] * move_length,  # S
    [-1, 0] * move_length,  # W
])

knight_move_vec = np.array([
    [1, 2],  # N
    [2, 1],  # NE
    [2, -1],  # E
    [1, -2],  # SE
    [-1, -2],  # S
    [-2, -1],  # SW
    [-2, 1],  # W
    [-1, 2]  # NW
])

promote_to = np.array([
    'Knight'
    'Rook'
    'Bishop'
])

def encode_board(last_six_board_nodes, color):
    """
    Encode the chess board into a numerical format suitable for neural network input.
    The encoding will have dimensions 8x8x12, where the first two dimensions represent
    the board squares, and the third dimension represents the one-hot encoding for the pieces.
    The order for one-hot encoding is [P, N, B, R, Q, K, p, n, b, r, q, k], where
    uppercase letters represent White pieces and lowercase Black pieces.
    """
    global index
    piece_to_index = {
        chess.PAWN: 0,
        chess.KNIGHT: 1,
        chess.BISHOP: 2,
        chess.ROOK: 3,
        chess.QUEEN: 4,
        chess.KING: 5
    }

    # Initialize a 8x8x12 array with zeros
    state_encoded = np.zeros((91, 8, 8))
    i = 0
    for state in last_six_board_nodes:
        if state.value is not None:
            for row in range(8):
                for col in range(8):
                    piece = state.value[row][col]
                    if piece != 0:
                        # Determine index in the third dimension
                        index = 14*i + piece
                        state_encoded[index, row, col] = 1
            repetitions = 0
            for prev in state.prevs:
                if prev == state:
                    repetitions += 1
            if repetitions == 1:
                state_encoded[(14 * i) + 13].fill(1)
            if repetitions == 2:
                state_encoded[14 * (i + 1)].fill(1)
        i += 1
    cur_state = last_six_board_nodes[0]
    state_encoded[index+1].fill((len(cur_state.prevs)) / 100)
    if cur_state.turn:
        state_encoded[index+2].fill(1)
    if cur_state.has_kingside_castling_rights(getattr(chess, color)):
        state_encoded[index+3].fill(1)
    if cur_state.has_queenside_castling_rights(getattr(chess, color)):
        state_encoded[index+4].fill(1)
    if cur_state.has_kingside_castling_rights(not getattr(chess, color)):
        state_encoded[index+5].fill(1)
    if cur_state.has_queenside_castling_rights(not getattr(chess, color)):
        state_encoded[index+6].fill(1)
    moves_since_progress = 0
    for i in range(len(cur_state.prevs)):
        if cur_state.prevs[i].hasCaptureOrPmove:
            moves_since_progress = i
            break
        else:
            moves_since_progress = i+1
    state_encoded[index+7].fill((moves_since_progress/50))




    return state_encoded
