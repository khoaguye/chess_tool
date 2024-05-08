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
        return "Illegal move"
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
    centipawn_value = calculate_centipawn1(fen)
    #print(f"Centipawn Value of the board before the move: {centipawn_value}")

    next_fen = get_next_fen(fen, move)
    if next_fen == "Illegal move":
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
    filePath = "output_4000_nl_model.csv"
    df = pd.read_csv(filePath)

    accuracy_percentages = []
    wrong_move = 0
    for index, row in df.iloc[1:].iterrows():
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
#print(str(accuracy_testing("2bk1bn1/3ppn1r/1p1q3p/r1p2Q2/p1N2Pp1/P1PP3N/1P2P1PP/R1B1KB1R w Q - 3 20", "c1d2")) + "%")

""" 
RESULT:

Model           Test case   Average    Median      Invalid move
5k FEN model        1000     23.4%      0               666
4k FEN model        800      12.2%      0               681
4k FEN model        1000     11.3%,     0               843
4k FEN nl model     1000     60.8%     89.75            261
"""

# def win_percent_from_cps(cp):
#     """ Convert centipawn difference to win percent using an exponential model. """
#     if cp >= 0:
#         return 100
#     else:
#         # The constants a, k, b are derived from your Scala code's embedded comment
#         return min(max(103.1668100711649 * np.exp(-0.04354415386753951 * cp) - 3.166924740191411 + 1, 0), 100)

# def accuracy_from_win_percents(before, after):
#     """ Calculate accuracy based on the win percentages before and after a move. """
#     return win_percent_from_cps(after - before)


# def accuracy_testing(fen, move):
#     move_accuracy = 0
#     centipawn_value = calculate_centipawn(fen, move)
#     #print(f"Centipawn Value of the board before the move: {centipawn_value}")

#     next_fen = get_next_fen(fen, move)
#     if next_fen == "Illegal move":
#         move_accuracy = 0
#     else:
#         centipawn_value = calculate_centipawn(fen, move)
#         print(f"Centipawn Value of the move: {centipawn_value}")

#         next_fen = get_next_fen(fen, move)
#         next_move= stockfish_fen_predict(next_fen)
#         centipawn_value_next = calculate_centipawn(next_fen,next_move)
#         print("Next FEN:", next_fen)

#         # Example usage:
#         cp_before = 0  # centipawn value before the move
#         cp_after = -50  # centipawn value after the move, indicating a loss

#         win_percent_before = win_percent_from_cps(centipawn_value)
#         win_percent_after = win_percent_from_cps(centipawn_value_next)
#         move_accuracy = accuracy_from_win_percents(win_percent_before, win_percent_after)

#         print(f"Move Accuracy: {move_accuracy}%")
#     return round(move_accuracy, 2)