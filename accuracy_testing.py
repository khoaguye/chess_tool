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
#print(get_next_fen("r5nr/6k1/n1p2ppp/1pP5/p4Pb1/P3P1PN/RPP1K1BP/2B2N1R w - - 2 25", "h3g5"))
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
            print("*****")
            return 0
        
        win_percent_before = win_percent_from_cps(centipawn_value)
        win_percent_after = win_percent_from_cps(centipawn_value_next)
        move_accuracy = accuracy_from_win_percents(win_percent_before, win_percent_after)
    
    if move_accuracy > 100:
        return 100
    return round(move_accuracy, 2)


def model_testing():
    filePath = "model_output/output_original_fen_4bit_lm3model.csv"
    df = pd.read_csv(filePath)

    accuracy_percentages = []
    wrong_move_list = []
    wrong_move = 0
    wrong_format_count = 0 
    invalid_fen_count = 0 
    
    for index, row in df.iloc[1:1001].iterrows():
        fen = row['FEN State']
        move = row['Move']
        # Track progress
        print(f"Processing row {index + 1}/{len(df)}: FEN = {fen}, Move = {move}")
        accuracy = accuracy_testing(fen, move)
        
        if accuracy == "wrong format":
            wrong_format_count += 1
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

    average_accuracy = statistics.mean(accuracy_percentages) if accuracy_percentages else 0
    median_accuracy = statistics.median(accuracy_percentages) if accuracy_percentages else 0

    # Write wrong moves to output.csv
    wrong_move_df = pd.DataFrame(wrong_move_list, columns=['Row Number', 'FEN', 'Move'])
    wrong_move_df.to_csv('wrong_move_output_11kv2.csv', index=False)
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
4k FEN model                 4000                800      12.2%      0               681             85.1%
4k FEN model                 4000                1000     11.3%,     0               843             84.3%
5k FEN model                 5000                1000     23.4%      0               666             66.6%
10k FEN model                10000               1999     31.2%      0               1181            59.0%
10k FEN model                10000               1000     30.4%      0               601             60.1%
11k FEN model                11000               1000     38.97%     1.71            484             48.4%

Model FEN 7x8B(4bit)  Num_of_train_data   Test case   Average    Median      Invalid move     Invalid move %    wrong_format
Based model               0                   1000     15.36%        0               457             45.7%              353
Based model 5shot         0                   1000     2.2%          0               970             97%                0
4k Fen model              4000                1000     12.4%         0               847             84.7%              1
7k Fen model              7000                1000     30.65%        0              
10k Fen model             10000               1000     39.27%       0.55            496              49.6%     
11k Fen model             11000               1000     50.67%       57.4            409              40.9%        
17k Fen model             17000               1000     61.55%       88.67           292              29.2               2
18k Fen model             18000               1000     61.69%       88.02           264              26.4               20
20k Fen model             20000               1000     61.28%       89.87           300              30.0%              2
22k Fen model             22000               1000     64.20%       90.35           258              25.8%              1  
23k Fen model             23000               1000     64.47%       87.51           241              24.1%              9          
24k Fen model             24000               1000     68.78%       95.99           209              20.9               2
25k Fen model             25000               1000     67.6%        95.2            226              22.6%              3      
27k                       27000               1000     71.12%       97.11           190              19.0                   2
30k Fen model             30000               1000     66.12%       93.4            237              23.7%              4


Model mixtral 7x8B NL (4bit)          Num_of_train_data   Test case   Average    Median      Invalid move       wrong_format
                Base                        0               1000        5.2       0              820                 116
                500                         500             1000        52.67     62.63          373                 0
                1k nl model                 1000            1000        54.71     71.61          348                 5
                5k                          5000            1000        63.49     89.66          262                 9
                7k                          7000            1000        70.35     97.17          206                 2
                10k                         10000           1000        73.63     97.17          161                 4
                11k                         11000           1000        73.10     97.56          165                 5                    
                13k                         13000           1000        73.97     97.94          160                 4                
                15k                         15000           1000        77.43     98.91          128                 3            
                17k                         17000           1000        76.98     98.61          131                 1    
                18k                         18000           1000        75.07     97.6           147                 2
                20k                         20000           1000        77.96     98.58          115                 4         

4k fEN nl model     1000     60.8%     89.75            261             26.1%
5k  

Model FEN LLama3(4bit) Num_of_train_data   Test case   Average     Median      Invalid move        wrong_format
4k Fen model              4000                1000     42.75%       18.03           493                  3
7k Fen model              7000                1000     49.56%       54.78           409                  5              
10k Fen model             10000               1000     62.85%       88.07           276                  3 
11k Fen model             11000               1000     59.44%       85.58           317                  4     
15k Fen model             15000               1000     65.89%       92.69           235                  3               
18k Fen model             18000               1000     69.23%       95.88           206                  1             
20k Fen model             20000               1000     70.29%       96.61           203                  2   
23k Fen model             23000               1000     70.50%       96.78           202                  2  
25k Fen model             25000               1000     71.30%       96.78           186                  3  



"""


        