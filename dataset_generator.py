from fen_generator import generate_random_fen
from stockfish_predict import stockfish_fen_predict
from convert_template import describe_fen, describe_next_move
import sys
import numpy as np
import csv
#from convert_template import get_next_fen, calculate_centipawn
import math




def generate(count=3000):
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
    #column-1 Instruction_fen
    Instruction_text = "You are a chess grandmaster. You understand and can locate chess pieces given the current state of the chess board in Forsyth-Edwards Notation (FEN). Given a board's state in FEN, your task is to consider factors such as material advantage, positional strength, and potential tactics like forks, pins, and discovered attacks to describe what next move would result in the best centipawn improvement for the active player. You will describe the move by giving a piece’s starting and ending coordinates (e.g., d4e5). Take extra care to only respond with a valid, legal move."

    #column-2 FEN_input
    FEN_input_text1 = "The board is in the following position: "
    FEN_input_text2 = ".What next move would produce the best centipawn improvement for the active player?"
    FEN_input = []

    #column-3 FEN_output
    FEN_output_text1= "The next move which would produce the best centipawn improvement for the active player of this fen state is: "
    FEN_output=[]

    #column-4 instruction_fen_nl
    Instruction_fen_nl_input= "You are a chess grandmaster. You understand and can locate chess pieces given the FEN state and the description of the current state of the chess board. Your task is to consider factors such as material advantage, positional strength, and potential tactics like forks, pins, and discovered attacks to find the next move that produces the best centipawn improvement for the active player. You will describe the move by giving a starting square of piece and ending square as coordinates of board . Take extra care to only use legal and valid moves."


    #column-5 FEN_and_Languages_ver
    FEN_and_Languages_ver_text1= "Here is the FEN state: "
    FEN_and_Languages_ver_text2= ". And here is the language version of the corresponding FEN state: "
    FEN_and_Languages_ver_text3= " What next move would produce the best centipawn improvement for the active player?"
    FEN_and_Languages_ver=[]

    nl_dataset=[]

    dataset = generate()
    if dataset:
        # fen = '4rbn1/p2q2p1/1n2k3/1ppNBp2/1P1P2p1/P6r/2PN1P1R/R2QK3 w Q - 0 22'; move= 'd5c7'
        fen_dataset = [fen for fen, move in dataset.items()]
        fen_dataset_with_next_move = []
        for fen, move in dataset.items():
            fen_next_move_str = "FEN state: " + fen + " ; Best move: " + move
            #column-8:  FEN state: rnbqkb1r/p2p1p1p/7n/2p5/PPpPpp2/2N5/3BPKPP/R2Q1BNR w kq - 0 9 ; Best move: d2f4
            fen_dataset_with_next_move.append(fen_next_move_str)

            fen_input_str = FEN_input_text1 + fen + FEN_input_text2
            #column-2: The board is in the following position: rnbqkb1r/p2p1p1p/7n/2p5/PPpPpp2/2N5/3BPKPP/R2Q1BNR w kq - 0 9. What next move would produce the best centipawn improvement for the active player?
            FEN_input.append(fen_input_str)

            fen_output_str= FEN_output_text1 + move
            #column-3: The next move which would produce the best centipawn improvement for the active player of this fen state is: a8a4
            FEN_output.append(fen_output_str)

            fen_and_Languages_ver_str= FEN_and_Languages_ver_text1 + fen + FEN_and_Languages_ver_text2 + describe_fen(fen) + FEN_and_Languages_ver_text3
            #column-5: Here is the FEN state: rnbqkb1r/p2p1p1p/7n/2p5/PPpPpp2/2N5/3BPKPP/R2Q1BNR w kq - 0 9. And here is the language version of its:
            # The current state of the chess board is: Black rook at a8, black knight at b8,
            # black bishop at c8, black queen at d8, black king at e8, black bishop at f8
            FEN_and_Languages_ver.append(fen_and_Languages_ver_str)

            # column-10 NL Format of FEN
            nl_dataset_input = describe_fen(fen) + FEN_and_Languages_ver_text3
            nl_dataset.append(nl_dataset_input)

        # column-9 instruction_nl
        Instruction_nl = "You are a chess grandmaster. Given a spoken-language description of a board's state, your task is to consider factors such as material advantage, positional strength, and potential tactics like forks, pins, and discovered attacks to describe what next move would result in the best centipawn improvement for the active player. You will describe the move by giving a piece’s starting and ending coordinates (e.g., d4e5). Take extra care to only respond with a valid, legal move."


        # column-11 Output for NLP
        FEN_output_for_nlp_text = "The next move which would produce the best centipawn improvement for the active player of this board state is "
        FEN_output_for_nlp = []

        #column-12
        nl_dataset_with_next_move = [describe_next_move(fen, move) for fen, move in dataset.items()]


        with open("test.csv", 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            #writer.writerow(['Instruction_fen','FEN_input','FEN_output','instruction_fen_nl','FEN_and_Languages_ver','FEN','output','FEN + Next move','instruction_nl','NL Format of FEN', 'Output for NLP','NL Format of FEN + Next move'])

            for index, text in enumerate(fen_dataset):
                f2=[]
                f3= fen_dataset_with_next_move[index].split("; Best move: ")
                output= f3[1]
                nl_output = "The next move which would produce the best centipawn improvement for the active player of this board state is " + output
                writer.writerow([Instruction_text, FEN_input[index], FEN_output[index],Instruction_fen_nl_input, FEN_and_Languages_ver[index],fen_dataset[index], output, fen_dataset_with_next_move[index], Instruction_nl,nl_dataset[index], nl_output, nl_dataset_with_next_move[index]])


    print('COMPLETE!')

    
    '''
    fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"  # Starting position
    move = "e2e4"
    centipawn_value = calculate_centipawn(fen, move)
    print(f"Centipawn Value of the move: {centipawn_value}")

    next_fen = get_next_fen(fen, move)
    next_move= stockfish_fen_predict(next_fen)
    centipawn_value_next = calculate_centipawn(next_fen,next_move)
    print("Next FEN:", next_fen)

    # Example usage:
    cp_before = 0  # centipawn value before the move
    cp_after = -50  # centipawn value after the move, indicating a loss

    win_percent_before = win_percent_from_cps(centipawn_value)
    win_percent_after = win_percent_from_cps(centipawn_value_next)
    move_accuracy = accuracy_from_win_percents(win_percent_before, win_percent_after)

    print(f"Move Accuracy: {move_accuracy}%")
    '''


