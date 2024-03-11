from fen_generator import generate_random_fen
from stockfish_predict import stockfish_fen_predict
from convert_template import describe_fen, describe_next_move
import sys
import csv


def generate(count=50):
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
        # fen = '4rbn1/p2q2p1/1n2k3/1ppNBp2/1P1P2p1/P6r/2PN1P1R/R2QK3 w Q - 0 22'; move= 'd5c7'
        fen_dataset = [fen for fen, move in dataset.items()]
        fen_dataset_with_next_move = []
        for fen, move in dataset.items():
            fen_str = "FEN state: " + fen + " ; Best move" + move
            fen_dataset_with_next_move.append(fen_str)

        nl_dataset = [describe_fen(fen) for fen in dataset]
        nl_dataset_with_next_move = [describe_next_move(fen, move) for fen, move in dataset.items()]



        with open("FEN DATABASE.csv", 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            #writer.writerow(['FEN','FEN + Next move','NL Format of FEN','NL Format of FEN + Next move'])
            for fen_dataset, fen_dataset_with_next_move, nl_dataset, nl_dataset_with_next_move in zip(fen_dataset, fen_dataset_with_next_move, nl_dataset, nl_dataset_with_next_move):
                writer.writerow([fen_dataset, fen_dataset_with_next_move, nl_dataset, nl_dataset_with_next_move])




