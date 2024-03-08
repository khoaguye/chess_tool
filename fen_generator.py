import chess
import random

DEFAULT_MIN_MOVES = 10
DEFAULT_MAX_MOVES = 50


def generate_random_fen(min_moves=DEFAULT_MIN_MOVES, max_moves=DEFAULT_MAX_MOVES):
    """
    Generates a random board state.
    :param min_moves: Minimum number of moves from starting position. Defaults to DEFAULT_MIN_MOVES.
    :param max_moves: Maximum number of moves from starting position. Defaults to DEFAULT_MAX_MOVES.
    :return: String representation of FEN board state
    """

    board = chess.Board()
    moves = random.randint(min_moves, max_moves)

    for _ in range(moves):
        legal_moves = list(board.legal_moves)
        if not len(legal_moves):
            break
        board.push(random.choice(legal_moves))

    return board.fen()


def batch_generate_fens(count=1000, min_moves=DEFAULT_MIN_MOVES, max_moves=DEFAULT_MAX_MOVES):
    """
    Generates a series of random board positions
    :param count: Total positions to generate
    :param min_moves: Minimum number of moves from starting position for each game. Defaults to DEFAULT_MIN_MOVES.
    :param max_moves: Maximum number of moves from the starting position for each game. Defaults to DEFAULT_MAX_MOVES.
    """
    for _ in range(count):
        print(generate_random_fen(min_moves, max_moves))


if __name__ == "__main__":
    batch_generate_fens()
