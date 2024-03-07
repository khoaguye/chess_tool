from stockfish import Stockfish
from dotenv import load_dotenv
import os

DEFAULT_STOCKFISH_THREADS = 4
DEFAULT_MIN_THINKING_TIME = 30
DEPTH = 18


def stockfish_fen_predict(fen_state, threads=DEFAULT_STOCKFISH_THREADS,
                          min_think_time=DEFAULT_MIN_THINKING_TIME):
    """
    Predicts the next best move using the installed stockfish designated by the environment variable STOCKFISH_FILEPATH.
    Raises ValueError on invalid FEN state.

    :param fen_state: string representation of FEN state
    :param threads: threads for stockfish
    :param min_think_time: minimum thinking time
    :return: A string of best move in algebraic notation or None if the current position is a mate
    """
    load_dotenv()

    # get stockfish installation
    stockfish_path = os.getenv("STOCKFISH_FILEPATH")
    if not stockfish_path or os.path.exists(stockfish_path):
        raise FileNotFoundError(f"Stockfish filepath not found: {stockfish_path}")

    # set up stockfish and load FEN position
    stockfish = Stockfish(stockfish_path, depth=DEPTH,
                          parameters={"Threads": threads, "Minimum Thinking Time": min_think_time})
    stockfish.set_fen_position(fen_state)

    # return best move in algebraic notation or None if next move is a mate
    if stockfish.is_fen_valid(fen_state):
        return stockfish.get_best_move()

    # raise error if fen_state is invalid
    raise ValueError(f"Invalid FEN state: {fen_state}")
