from flask import Flask, request, jsonify
from flask_cors import CORS
from model import ChessAI
import chess

app = Flask(__name__)
CORS(app)

# Initialize the AI model
ai = ChessAI()

@app.route('/', methods=['GET'])
def index():
    return "Chess AI Backend is Running!", 200

@app.route('/move', methods=['POST'])
def move():
    data = request.json
    fen = data['fen']

    board = chess.Board(fen)
    move = ai.predict_move(board)
    board.push(move)

    response = {
        'move': move.uci(),
        'fen': board.fen()
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
