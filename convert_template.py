# Define the FEN string
# Define the FEN string (Make sure there's no leading or trailing whitespace)
fen_string = "r1bqkb1r/1p1ppppp/7n/p1p5/1n1P4/1PP1B3/P1Q1PPPP/RN2KBNR b KQkq - 2 8".strip()


# Define a dictionary to map FEN pieces to their names
piece_names = {
    'r': 'rook',
    'n': 'knight',
    'b': 'bishop',
    'q': 'queen',
    'k': 'king',
    'p': 'pawn',
    'R': 'rook',
    'N': 'knight',
    'B': 'bishop',
    'Q': 'queen',
    'K': 'king',
    'P': 'pawn',
}

# Define a function to describe the board state
def describe_fen(fen_string):
    description = ""
    # Split the FEN string into components
    fen_components = fen_string.split(' ')
    fen_board = fen_components[0]  # Extract the board state from FEN

    # Iterate over the FEN board
    row_index = 0
    for char in fen_board:
        if char == '/':
            # Move to the next row
            row_index += 1
        elif char.isdigit():
            # Skip empty squares denoted by digits
            pass
        else:
            # Determine the position and piece name
            col_index = fen_board.index(char)
            position = f"{chr(ord('a') + col_index)}{8 - row_index}"
            piece = piece_names[char]
            description += f"At position {position}, piece is {piece}. "

    return description.strip()  # Remove trailing space if any

# Print the description of the FEN string
print(describe_fen(fen_string))
