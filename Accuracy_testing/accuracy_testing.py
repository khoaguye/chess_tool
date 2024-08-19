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
    pattern = r'^[a-h][1-8][a-h][1-8]$'
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
            return abs(score)
        else:
            raise ValueError("Evaluation result does not contain 'value'.")
    except StockfishException as e:
        print(f"Stockfish exception occurred: {e}")
        return None

# Function to calculate the accuracy of a move based on FEN state and UCI move
def accuracy_testing(fen, move):
    if not isinstance(move, str):
        move = str(move)
    if move == "":
        return 0
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
        
        if centipawn_value_next is None or isinstance(centipawn_value_next, str):
            return 0
        
        win_percent_before = win_percent_from_cps(centipawn_value)
        win_percent_after = win_percent_from_cps(centipawn_value_next)
        move_accuracy = accuracy_from_win_percents(win_percent_before, win_percent_after)
    
    if move_accuracy > 100:
        return 100
    return round(move_accuracy, 2)


def model_testing(filePath):
    df = pd.read_csv(filePath)

    accuracy_percentages = []
    wrong_move_list = []      
    wrong_move = 0
    wrong_format_count = 0 
    invalid_fen_count = 0 
    wrong_format_arr = []
    no_match_found_count = 0
    for index, row in df.iloc[0:1001].iterrows():
        fen = row['FEN State']
        move = row['Move']
        # Track progress                                                                                
        print(f"Processing row {index + 1}/{len(df)}: FEN = {fen}, Move = {move}")
        if move == "No match found":
            no_match_found_count += 1 
            accuracy_percentages.append(0)
            continue

        accuracy = accuracy_testing(fen, move)
        
        if accuracy == "wrong format":
            wrong_format_count += 1
            wrong_format_arr.append((index,fen,move))
            accuracy_percentages.append(0)
        elif accuracy == "invalid_fen_state":
            invalid_fen_count += 1
            accuracy_percentages.append(0)
        elif accuracy == 0:                     
            wrong_move += 1                         
            wrong_move_list.append([index, fen, move])              
            accuracy_percentages.append(0)              
        else:                       
            accuracy_percentages.append(accuracy)   
        #print(accuracy_percentages) 
    average_accuracy = statistics.mean(accuracy_percentages) if accuracy_percentages else 0
    median_accuracy = statistics.median(accuracy_percentages) if accuracy_percentages else 0
                            
    return (average_accuracy, median_accuracy, wrong_move, wrong_format_count, invalid_fen_count, wrong_format_arr ,no_match_found_count)



# Loop through shot numbers and compile results
results = []
for shot in range(1,10):
    print(shot)
    filePath = "<input dir>"
    average_accuracy, median_accuracy, wrong_move, wrong_format_count, invalid_fen_count, wrong_format_arr, no_match_found_count = model_testing(filePath)
    results.append({
        "Model": "FEN 8x7B(4bit)",
        "Num_of_train_data": f"{shot}shot",
        "Test case": 1000,
        "Average": average_accuracy,
        "Median": median_accuracy,
        "Invalid move": wrong_move,
        "wrong_format": wrong_format_count,
        "No output": no_match_found_count
    })

# Convert results to DataFrame and save to CSV
results_df = pd.DataFrame(results)
output_file_path = "<output dir>"
results_df.to_csv(output_file_path, index=False)

print(f"Results saved to {output_file_path}")


