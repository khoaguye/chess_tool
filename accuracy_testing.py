from stockfish import Stockfish, StockfishException
from dotenv import load_dotenv
import os
import pandas as pd
import statistics
import chess
import re
import math

# Load environment variables
load_dotenv()

# Utility function to check if FEN is valid
def is_valid_fen(fen):
    try:
        chess.Board(fen)
        return True
    except ValueError:
        return False

# Function to validate and apply a move to a FEN state
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

# Function to convert centipawn score to win percentage
def win_percent_from_cps(cp):
    win_percentage = 50 + 50 * (2 / (1 + math.exp(-0.00368208 * cp)) - 1)
    return win_percentage

# Function to calculate move accuracy based on win percentages before and after the move
def accuracy_from_win_percents(before, after):
    accuracy_percentage = 103.1668 * math.exp(-0.04354 * (before - after)) - 3.1669
    return accuracy_percentage

# Function to calculate the centipawn value for a given FEN using Stockfish
def calculate_centipawn1(fen):
    stockfish_path = os.getenv("STOCKFISH_FILEPATH")
    
    if not stockfish_path or not os.path.isfile(stockfish_path):
        raise ValueError("Stockfish executable not found at the specified path.")
    
    stockfish = Stockfish(stockfish_path)
    
    if not is_valid_fen(fen):
        return "invalid_fen_state"
    
    try:
        stockfish.set_fen_position(fen)
        evaluation = stockfish.get_evaluation()
        if 'value' in evaluation:
            score = evaluation['value']
            return score
        else:
            raise ValueError("Evaluation result does not contain 'value'.")
    except StockfishException as e:
        print(f"Stockfish exception occurred: {e}")
        return None

# Function to calculate the accuracy of a move based on FEN state and UCI move
def accuracy_testing(fen, move):
    move_accuracy = 0
    centipawn_value = calculate_centipawn1(fen)
    
    if centipawn_value == "invalid_fen_state":
        return "invalid_fen_state"
    
    if centipawn_value is None:
        return 0
    
    next_fen = get_next_fen(fen, move)
    if next_fen == "wrong format":
        return "wrong format"
    elif next_fen == "Illegal move":
        return 0
    else:
        centipawn_value_next = calculate_centipawn1(next_fen)
        
        if centipawn_value_next is None:
            return 0
        
        win_percent_before = win_percent_from_cps(centipawn_value)
        win_percent_after = win_percent_from_cps(centipawn_value_next)
        move_accuracy = accuracy_from_win_percents(win_percent_before, win_percent_after)
    
    return min(100, round(move_accuracy, 2))

# Function to test the model based on a dataset
def model_testing():
    filePath = "output_20000_fen_4bit_model.csv"
    df = pd.read_csv(filePath)

    accuracy_percentages = []
    wrong_move = 0
    wrong_format_count = 0
    invalid_fen_count = 0
    
    for index, row in df.iloc[1:1001].iterrows():
        fen = row['FEN State']
        move = row['Move']
        # Track progress
        print(f"Processing row {index + 1}/{len(df)}: FEN = {fen}, Move = {move}")
        accuracy = accuracy_testing(fen, move)
        
        if accuracy == 0:
            wrong_move += 1
        elif accuracy == "wrong format":
            wrong_format_count += 1
        elif accuracy == "invalid_fen_state":
            invalid_fen_count += 1
        else:
            accuracy_percentages.append(accuracy)

    average_accuracy = statistics.mean(accuracy_percentages) if accuracy_percentages else 0
    median_accuracy = statistics.median(accuracy_percentages) if accuracy_percentages else 0

    return (average_accuracy, median_accuracy, wrong_move, wrong_format_count, invalid_fen_count)




# Run the model testing and print results
average_accuracy, median_accuracy, wrong_move, wrong_format_count, invalid_fen_count = model_testing()
print(f"Average Accuracy: {average_accuracy}")
print(f"Median Accuracy: {median_accuracy}")
print(f"Wrong Moves: {wrong_move}")
print(f"Wrong Format Moves: {wrong_format_count}")
print(f"Invalid FEN States: {invalid_fen_count}")



""" 
RESULT:

Model (16bit)          Num_of_train_data   Test case   Average    Median      Invalid move     Invalid move %
4k FEN model        4000                800      12.2%      0               681             85.1%
4k FEN model        4000                1000     11.3%,     0               843             84.3%
5k FEN model        5000                1000     23.4%      0               666             66.6%
10k FEN model       10000               1999     31.2%      0               1181            59.0%
10k FEN model       10000               1000     30.4%      0               601             60.1%
11k FEN model       11000               1000     38.97%     1.71            484             48.4%

Model (4bit)          Num_of_train_data   Test case   Average    Median      Invalid move     Invalid move %    wrong_format
4k Fen model              4000                1000     11.28%     0               847             84.7%    
10k Fen model             10000               1000     39.27%     0.55            496             49.6%
11k Fen model             11000               1000     47.43%     38.46           409             40.9%        
20k Fen model             20000               1000     82.39%     100             298                               2


4k FEN nl model     1000     60.8%     89.75            261             26.1%
"""


        