from fen_generator import generate_random_fen
from stockfish_predict import stockfish_fen_predict
import sys


def generate(count=10):
    # TODO add documentation
    output = {}
    warnings = 0

    for _ in range(count):
        fen_state = generate_random_fen()
        try:
            best_move = stockfish_fen_predict(fen_state)
        except ValueError as e:
            print(f"WARNING: {e}", file=sys.stderr)
            continue
        except FileNotFoundError:
            print('ERROR: Unable to locate Stockfish installation.', file=sys.stderr)
            exit(2)

        if best_move:
            output[fen_state] = best_move
        else:
            print(f"WARNING: The position '{fen_state}' is already in checkmate.", file=sys.stderr)
            warnings += 1
    return output


# TODO create a function to convert output of generate() to csv

if __name__ == "__main__":
    dataset = generate()
    if dataset:
        for fen, move in dataset:
            print(f"FEN state: '{fen}'\nBest move: {move}")
