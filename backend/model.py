import numpy as np
import chess
import chess.engine

class ChessAI:
    def __init__(self):
        try:
            # Use the system-installed Stockfish
            self.engine = chess.engine.SimpleEngine.popen_uci("/usr/games/stockfish")
        except Exception as e:
            print(f"Error initializing Stockfish: {e}")
            raise

    def board_to_tensor(self, board):
        # Implement board representation
        tensor = np.zeros((8, 8, 12), dtype=int)
        piece_map = board.piece_map()
        for square, piece in piece_map.items():
            row = 7 - (square // 8)
            col = square % 8
            idx = self.piece_to_index(piece)
            tensor[row, col, idx] = 1
        return tensor

    def piece_to_index(self, piece):
        piece_type = piece.piece_type
        color = int(piece.color)
        return (piece_type - 1) + (6 * color)


    def predict_move(self, board):
        try:
            # Set a time limit for the engine
            result = self.engine.play(board, chess.engine.Limit(time=0.1))
            return result.move
        except Exception as e:
            print(f"Error making move: {e}")
            raise

    def __del__(self):
        try:
            if hasattr(self, 'engine'):
                self.engine.quit()
        except Exception as e:
            print(f"Error closing engine: {e}")