import chess
import chess.engine
import os
from stockfish import Stockfish
from dotenv import load_dotenv
import os
import re

DEFAULT_FEN_STATE = "5rk1/1p3ppp/pq3b2/8/3Q4/1P3N2/P4PPP/3R2K1 b KQ - 3 27"
# Define a dictionary to map FEN pieces to their names
PIECE_NAMES = {
    'r': 'rook',
    'n': 'knight',
    'b': 'bishop',
    'q': 'queen',
    'k': 'king',
    'p': 'pawn',
}


# Define a function to describe the board state
def describe_fen(fen_string=DEFAULT_FEN_STATE):
    """
    Convert Fen notation to english
    :param fen_string: the generated fen string, represent the current state of the board
    :return description: the description include the current board state, castling, en passant, half move number and full move number
    :example:
        input: "5rk1/1p3ppp/pq3b2/8/3Q4/1P3N2/P4PPP/3R2K1 b - - 3 27"
        output: The current chess state is: rook at (8, f).king at (8, g).pawn at (7, b).pawn at (7, f).pawn at (7, g).pawn at (7, h).pawn at (6, a).queen at (6, b).bishop at (6, f).queen at (4, d).pawn at (3, b).knight at (3, f).pawn at (2, a).pawn at (2, f).pawn at (2, g).pawn at (2, h).rook at (1, d).king at (1, g).
                The next player is Black
                Half move number is 3
                Full move number is 27
    """

    fen_components = fen_string.split(' ')

    description = "The current state of the chess board is: "
    description += describe_board(fen_components)
    description += process_castles(fen_components)
    description += process_half_full_moves(fen_components)
    description += process_en_passant(fen_components)
    description += get_next_player(fen_components)

    return description


def process_en_passant(fen_components):
    # TODO implement en passant
    en_passant_target = fen_components[3]

    if en_passant_target != '-':
        return f"En Passant Target Square: {en_passant_target}. "
    return ""


def process_half_full_moves(fen_components):
    # TODO implement half/full moves
    output = ""
    output += f"Half move number is {fen_components[4]}. "
    output += f"Full move number is {fen_components[5]}. "
    return output


def describe_board(fen_components):
    output = ""

    # Split the FEN string into ranks
    ranks = fen_components[0].split('/')

    # Loop through each rank
    for row, rank in enumerate(ranks):
        col = 0
        row_string = ""

        # skip if empty rank
        if rank == "8":
            continue

        # Loop through each character in the rank
        for piece_char in rank:
            if piece_char.isdigit():
                col += int(piece_char)  # If it's a number, move the column by that number
            else:
                color = "white" if piece_char.isupper() else "black"
                piece_name = PIECE_NAMES[piece_char.lower()]  # Get the piece name
                row_string += f"{color} {piece_name} at {chr(col + ord('a'))}{8 - row}, "
                col += 1  # Move to the next column
        output += " and ".join(row_string.rstrip(", ").rsplit(", ", 1)).capitalize() + ". "
    return output


def process_castles(fen_components):
    output = ""

    castling_info = fen_components[2]
    if fen_components[2] != '-':
        castling_availability = []
        if 'K' in castling_info:
            castling_availability.append("white kingside")
        if 'Q' in castling_info:
            castling_availability.append("white queenside")
        if 'k' in castling_info:
            castling_availability.append("black kingside")
        if 'q' in castling_info:
            castling_availability.append("black queenside")

        if len(castling_availability) == 1:
            output += f"{castling_availability[0]} is the only castle move available. ".capitalize()
        else:
            output += (", ".join(castling_availability[:-2]) + ", " + " and ".join(
                castling_availability[-2:]) if len(castling_availability) > 2 else " and ".join(
                castling_availability)).capitalize() + " castles are available. "
    else:
        output += "Both players have exhausted their castles. "

    return output


def get_next_player(fen_components):
    return ("White" if fen_components[1] == "w" else "Black") + " to move."

def describe_next_move(fen_string, algebraic_notation):
    if len(algebraic_notation) != 4:
        return "Invalid algebraic notation. It should be in the format 'e.g. c1e3'."

    piece = algebraic_notation[0]
    start_square = algebraic_notation[0:2]
    end_square = algebraic_notation[2:]

    natural_language = (f"Input: {describe_fen(fen_string)} ; "
                        f"Output: Move from {start_square} to {end_square}.")
    return natural_language


# def calculate_centipawn(fen, move):
#     # Path to the Stockfish engine executable

#     load_dotenv()

#     # get stockfish installation
#     stockfish_path = os.getenv("STOCKFISH_FILEPATH")

#     # Set up the chess board and engine
#     board = chess.Board(fen)
#     engine = chess.engine.SimpleEngine.popen_uci(stockfish_path)

#     # Evaluate the position before the move
#     info_before = engine.analyse(board, chess.engine.Limit(depth=20))
#     score_before = info_before['score'].relative.score(mate_score=100000)

#     # Make the move on the board
#     move = chess.Move.from_uci(move)
#     board.push(move)

#     # Evaluate the position after the move
#     info_after = engine.analyse(board, chess.engine.Limit(depth=20))
#     score_after = info_after['score'].relative.score(mate_score=100000)

#     # Calculate the centipawn change
#     centipawn_change = score_after - score_before

#     engine.quit()

#     return centipawn_change


# def calculate_centipawn(fen):
#     # Path to the Stockfish engine executable
#     #     # Path to the Stockfish engine executable

#     load_dotenv()

#     # get stockfish installation
#     stockfish_path = os.getenv("STOCKFISH_FILEPATH")

#     # Set up the chess board and engine
#     board = chess.Board(fen)
#     engine = chess.engine.SimpleEngine.popen_uci(stockfish_path)
#     load_dotenv()

#     # get stockfish installation
#     stockfish_path = os.getenv("STOCKFISH_FILEPATH")
#     info_before = engine.analyse(board, chess.engine.Limit(depth=20))
#     print(info_before['score'])
#     #score_after = info_after['score'].relative.score(mate_score=100000)
#     stockfish = Stockfish(stockfish_path)
#     stockfish.set_fen_position(fen)
#     score = stockfish.get_evaluation()['value']

   

#     #return centipawn_change
#     return score


def get_next_fen(fen, move_uci):
    board = chess.Board(fen)
    move = chess.Move.from_uci(move_uci)
    pattern = r'^[a-z]\d[a-z]\d$'
    if not re.match(pattern, move_uci):
        return "Illegal move"
    else:
        if move in board.legal_moves:  # Check if the move is legal
            board.push(move)
            return board.fen()
        else:
            return "Illegal move"


# Test the function
