import chess
import chess.engine
from dotenv import load_dotenv
import os
def evaluate_move(fen, move):

    load_dotenv()
    # get stockfish installation
    stockfish_path = os.getenv("STOCKFISH_FILEPATH")
    if not stockfish_path or not os.path.exists(stockfish_path):
        raise FileNotFoundError(f"Stockfish filepath not found: {stockfish_path}")
    board = chess.Board(fen)
    engine = chess.engine.SimpleEngine.popen_uci(stockfish_path)  

    # Get the Stockfish evaluation score
    info = engine.analyse(board, chess.engine.Limit(time=0.1))
    score = info['score']
    # if isinstance(score, chess.engine.Mate):
    #     score_advantage = score.relative.Mate
    # else:
    #     # Interpret the score (
    score_advantage = score.relative.cp
    interpretation = ""
    if score_advantage > 0:
      interpretation = "White is slightly better" if abs(score_advantage) <= 50 else (
          "White is winning" if score_advantage > 200 else "White has a significant advantage"
      )
    elif score_advantage < 0:
      interpretation = "Black is slightly better" if abs(score_advantage) <= 50 else (
          "Black is winning" if score_advantage < -200 else "Black has a significant advantage"
      )
    else:
      interpretation = "Equal position"
    engine.quit()
    return score_advantage, interpretation

  
fen = "4r1k1/4ppP1/p2p4/2p3b1/2P1R3/6Q1/q1P2PPK/1r6 b - - 3 27"
move = "a2c2"

centipawn_advantage, interpretation = evaluate_move(fen, move)

print(f"Move: {move}")
print(f"Evaluation: {centipawn_advantage} centipawns")
print(f"Interpretation: {interpretation}")


"""
import chess
import chess.engine
from dotenv import load_dotenv
import os

DEFAULT_FEN = "r1bqkb1r/ppp2ppp/2p5/4p3/4n2P/5N1R/PPPP1PP1/RNBQK3 b Qkq - 1 6"

def rate_move(fen=DEFAULT_FEN):
    load_dotenv()

    # Get Stockfish installation path
    stockfish_path = os.getenv("STOCKFISH_FILEPATH")
    engine = chess.engine.SimpleEngine.popen_uci(stockfish_path)

    # Create a chess board
    board = chess.Board(fen)

    # Analyze the position before the move
    initial_info = engine.analyse(board, chess.engine.Limit(depth=20, time=1.0))
    initial_score = initial_info["score"].relative.cp
    print(initial_score)
    # Make the move
    move = chess.Move.from_uci("g2g3")
    board.push(move)

    # Analyze the position after the move
    new_info = engine.analyse(board, chess.engine.Limit(depth=20, time=1.0))
    #new_scores = new_info["score"]
    new_score = new_info["score"].relative.cp
    print(new_score)
    # Compute the difference in scores
    score_difference = new_score - initial_score
    print(score_difference)
    # Quit the engine
    engine.quit()

    #return score_difference
rate_move()
# if __name__ == "__main__":
#     move_score_difference = rate_move()
#     print(f"Score Difference: {move_score_difference}")





from stockfish import Stockfish
import chess
import chess.engine
from dotenv import load_dotenv
import os

DEFAULT_STATE_BOARD = "r2qr1k1/4ppb1/p2p1np1/1pp3p1/2B5/P1NP1Q1P/1PP2PP1/R3R1K1 w - - 0 16"
DEFAULT_MOVE = "c4b3"
DEFAULT_STOCKFISH_THREADS = 4
DEFAULT_MIN_THINKING_TIME = 30
DEPTH = 18
def rate_move(fen=DEFAULT_STATE_BOARD, new_move = DEFAULT_MOVE,  threads=DEFAULT_STOCKFISH_THREADS,
                          min_think_time=DEFAULT_MIN_THINKING_TIME):
    load_dotenv()

     # get stockfish installation
    stockfish_path = os.getenv("STOCKFISH_FILEPATH")
    if not stockfish_path or not os.path.exists(stockfish_path):
        raise FileNotFoundError(f"Stockfish filepath not found: {stockfish_path}")
    
    # set up stockfish and load FEN position
    stockfish = Stockfish(stockfish_path, depth=DEPTH,
                          parameters={"Threads": threads, "Minimum Thinking Time": min_think_time})
    # Create a chess board with current fen 
    board = chess.Board(fen)
    #add new move to board 
    move = chess.Move.from_uci(new_move)
    board.push(move)
    stockfish.set_fen_position(board.fen())
    #Get the evaluation score (Positive is advantage white, negative is advantage black, the higher the better)
    eval = stockfish.get_evaluation()
    return eval
print(rate_move())

"""
