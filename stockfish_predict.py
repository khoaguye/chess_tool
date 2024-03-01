from stockfish import Stockfish
from dotenv import load_dotenv
import os
def stockfish_predict():
    # Update the path to your Stockfish binary
    load_dotenv() 

    filePath = os.getenv("filePath") 
    stockfish = Stockfish(filePath, depth=18, parameters={"Threads": 4, "Minimum Thinking Time": 30})  
    fen_state = "rnbqkbnr/ppp2ppp/8/3pp3/2P3P1/8/PP1PPP1P/RNBQKBNR w KQkq - 0 3"
    stockfish.set_fen_position(fen_state)
    if stockfish.is_fen_valid(fen_state):
        move = stockfish.get_best_move()
        return move 
    else:
        print('Fen state is incorrect')

if __name__ == "__main__":
    print(stockfish_predict())