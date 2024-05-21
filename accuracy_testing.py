#from convert_template import get_next_fen
from stockfish_predict import stockfish_fen_predict
from stockfish import Stockfish
from dotenv import load_dotenv
import os
import pandas as pd
import statistics
import chess
import re
import math

"""
Predicts the next best move using the installed stockfish designated by the environment variable STOCKFISH_FILEPATH.
Raises ValueError on invalid FEN state.

:param fen: String representation of the FEN state.
:param move_uci: String representation of the move in UCI notation.
:return: The next FEN state after the move if legal, "Illegal move" if the move is not in the correct format or not legal, and "Invalid UCI format" if the UCI format is invalid.
"""
def get_next_fen(fen, move_uci):
    board = chess.Board(fen)
    pattern = r'^[a-z]\d[a-z]\d$'
    if not re.match(pattern, move_uci):
        return "wrong format"
    else:
        try:
            move = chess.Move.from_uci(move_uci)
            if move in board.legal_moves:
                board.push(move)
                return board.fen()
            else:
                return "Illegal move"
        except ValueError:
            return "Invalid UCI format"

"""
Calculates the win percentage based on the centipawn score using a logistic function.

:param cp: Integer representing the centipawn score.
:return: Float representing the win percentage.
"""
def win_percent_from_cps(cp):
    win_percentage = 50 + 50 * (2 / (1 + math.exp(-0.00368208 * cp)) - 1)
    return win_percentage

"""
Calculates the accuracy of a move based on the win percentages before and after a move.

:param before: Float representing the win percentage before the move.
:param after: Float representing the win percentage after the move.
:return: Float representing the accuracy percentage.
"""
def accuracy_from_win_percents(before, after):
    #Calculate accuracy based on the win percentages before and after a move.
    accuracy_percentage = 103.1668 * math.exp(-0.04354 * (before - after)) - 3.1669
    return accuracy_percentage

"""
Calculates the centipawn value for a given board state using Stockfish engine.

:param fen: String representation of the FEN state.
:return: Integer representing the centipawn value of the board evaluation.
"""
def calculate_centipawn1(fen):
    # Path to the Stockfish engine executable
    #     # Path to the Stockfish engine executable

    load_dotenv()

    # get stockfish installation
    stockfish_path = os.getenv("STOCKFISH_FILEPATH")

    load_dotenv()

    # get stockfish installation
    stockfish_path = os.getenv("STOCKFISH_FILEPATH")
 
    stockfish = Stockfish(stockfish_path)
    stockfish.set_fen_position(fen)
    score = stockfish.get_evaluation()['value']

    return score


"""
Calculates the accuracy of a move based on the win percentages before and after a move, considering the FEN state and the move in UCI notation.

:param fen: String representation of the FEN state.
:param move: String representation of the move in UCI notation.
:return: Float representing the accuracy percentage.
""" 
def accuracy_testing(fen, move):
    move_accuracy = 0
    wrong_format = 0
    centipawn_value = calculate_centipawn1(fen)
    #print(f"Centipawn Value of the board before the move: {centipawn_value}")

    next_fen = get_next_fen(fen, move)
    if next_fen == "wrong format":
        wrong_format += 1
        move_accuracy = 0
    elif next_fen == "Illegal move":
        move_accuracy = 0
    else:
        #print((fen, move))
        centipawn_value_next = calculate_centipawn1(next_fen)
        #print("Next FEN:", next_fen)

        win_percent_before = win_percent_from_cps(centipawn_value)
       #print(win_percent_before)
        win_percent_after = win_percent_from_cps(centipawn_value_next)
        #print(win_percent_after)
        move_accuracy = accuracy_from_win_percents(win_percent_before, win_percent_after)
    if move_accuracy > 100:
        return 100
    return round(move_accuracy, 2)

"""
Tests the accuracy of moves based on a given dataset and returns statistical information.

:return: Tuple containing the average accuracy, median accuracy, and count of wrong moves.
"""
def model_testing():
    filePath = "output_11000_fen_model.csv"
    df = pd.read_csv(filePath)

    accuracy_percentages = []
    wrong_move = 0
    for index, row in df.iloc[1:1001].iterrows():
        fen = row['FEN State']
        move = row['Move']
        accuracy = accuracy_testing(fen, move)
        if accuracy == 0:
            wrong_move += 1
        accuracy_percentages.append(accuracy)

    # Calculate statistics
    average_accuracy = statistics.mean(accuracy_percentages)
    median_accuracy = statistics.median(accuracy_percentages)

    return (average_accuracy, median_accuracy, wrong_move)
print(model_testing())
# if __name__ == "__main__":
#     print(model_testing())
""" 
RESULT:

Model           Num_of_train_data   Test case   Average    Median      Invalid move     Invalid move %
4k FEN model        4000                800      12.2%      0               681             85.1%
4k FEN model        4000                1000     11.3%,     0               843             84.3%
5k FEN model        5000                1000     23.4%      0               666             66.6%
10k FEN model       10000               1999     31.2%      0               1181            59.0%
10k FEN model       10000               1000     30.4%      0               601             60.1%
11k FEN model       11000               1000     38.97%     1.71            484             48.4%
4k FEN nl model     1000     60.8%     89.75            261             26.1%
"""


        