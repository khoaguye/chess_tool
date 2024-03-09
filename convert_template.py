
fen_string = "5rk1/1p3ppp/pq3b2/8/3Q4/1P3N2/P4PPP/3R2K1 b - - 3 27"

# Define a function to describe the board state
def describe_fen(fen_string):
    """
    Convert Fen notaiton to english
    :param fen_string: the generated fen string, represent the current state of the board
    :return description: the description include the current board state, castling, en passant, half move number and full move number
    :example:
        input: "5rk1/1p3ppp/pq3b2/8/3Q4/1P3N2/P4PPP/3R2K1 b - - 3 27"
        output: The current chess state is: rook at (8, f).king at (8, g).pawn at (7, b).pawn at (7, f).pawn at (7, g).pawn at (7, h).pawn at (6, a).queen at (6, b).bishop at (6, f).queen at (4, d).pawn at (3, b).knight at (3, f).pawn at (2, a).pawn at (2, f).pawn at (2, g).pawn at (2, h).rook at (1, d).king at (1, g).
                The next player is Black
                Half move number is 3
                Full move number is 27
    """
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
    description = "The current chess state is: "
    fen_components = fen_string.split(' ')
    fen_board = fen_components[0]  # Extract the board state from FEN

    # Split the FEN string into ranks
    ranks = fen_board.split('/')

    # Loop through each rank
    for row, rank in enumerate(ranks):
        col = 0
        # Loop through each character in the rank
        for char in rank:
            if char.isdigit():
                col += int(char)  # If it's a number, move the column by that number
            else:
                piece_name = piece_names[char.lower()]  # Get the piece name
                description += f"{piece_name} at ({8 - row}, {chr(col + ord('a'))})."
                col += 1  # Move to the next column
    # next player description
    next_player = fen_components[1]
    if next_player == "w":
        description += "\nThe next player is White"
    elif next_player == "b":
        description += "\nThe next player is Black"
    
    #castling_info description
    castling_info = fen_components[2]
    if castling_info != '-':
        description += "\nCastling Availability: "
        if 'K' in castling_info:
            description += "White kingside, "
        if 'Q' in castling_info:
            description += "White queenside, "
        if 'k' in castling_info:
            description += "Black kingside, "
        if 'q' in castling_info:
            description += "Black queenside, "
        description = description.rstrip(', ') 
    
    #En passant description
    en_passant_target = fen_components[3]
    if en_passant_target != '-':
        description += f"\nEn Passant Target Square: {en_passant_target}"
    
    # half move and full move description
    half_move = fen_components[4]
    full_move = fen_components[5]
    description += f"\nHalf move number is {half_move}"
    description += f"\nFull move number is {full_move}"
    return description

# Test the function
if __name__ == "__main__":
    print(describe_fen(fen_string))
