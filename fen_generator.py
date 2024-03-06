import chess
import random

def generate_random_fen():
    board = chess.Board()
    moves = random.randint(10, 50)  # Generate random number of moves
    for _ in range(moves):
        legal_moves = list(board.legal_moves)
        if len(legal_moves) == 0:
            break
        move = random.choice(legal_moves)
        board.push(move)
    return board.fen()

def main():
    num_positions = 1000
    random_fens = [generate_random_fen() for _ in range(num_positions)]
    for fen in random_fens:
        print(fen)

if __name__ == "__main__":
    main()