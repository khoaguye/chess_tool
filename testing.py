from dataset_generator import accuracy_from_win_percents
from dataset_generator import win_percent_from_cps
from stockfish_predict import stockfish_fen_predict
from stockfish import Stockfish
from dotenv import load_dotenv
import os
import pandas as pd
import statistics
import chess

def get_next_fen(fen, move_uci):
    board = chess.Board(fen)
    move = chess.Move.from_uci(move_uci)

    if move in board.legal_moves:  # Check if the move is legal
        board.push(move)
        return board.fen()
    else:
        return "Illegal move"

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


#Accuracy represent how much your move deviated from the best moves. 
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