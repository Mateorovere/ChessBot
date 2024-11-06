import numpy as np
import chess
import random
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, Dense, Flatten, Input
from tensorflow.keras.optimizers import Adam

class ChessAITrainer:
    def __init__(self):
        self.model = self.build_model()
        self.gamma = 0.95  # Discount factor

    def build_model(self):
        input_layer = Input(shape=(8, 8, 12))
        x = Conv2D(64, (3, 3), activation='relu')(input_layer)
        x = Flatten()(x)
        x = Dense(128, activation='relu')(x)
        output_layer = Dense(1, activation='tanh')(x)
        model = tf.keras.Model(inputs=input_layer, outputs=output_layer)
        model.compile(optimizer=Adam(learning_rate=0.001), loss='mean_squared_error')
        return model

    def train(self, episodes=100000):
        for episode in range(episodes):
            board = chess.Board()
            states = []
            rewards = []

            while not board.is_game_over():
                tensor = self.board_to_tensor(board)
                states.append(tensor)

                legal_moves = list(board.legal_moves)
                move = random.choice(legal_moves)
                board.push(move)

                reward = self.evaluate_reward(board)
                rewards.append(reward)

            # Compute discounted rewards
            discounted_rewards = self.discount_rewards(rewards)
            states = np.array(states)
            discounted_rewards = np.array(discounted_rewards)

            # Ensure that states and rewards do not contain None values
            assert None not in states, "States contain None values"
            assert None not in discounted_rewards, "Rewards contain None values"

            self.model.fit(states, discounted_rewards, epochs=1, verbose=0)

            if episode % 100 == 0:
                print(f"Episode {episode} completed")

        self.model.save('models/checkpoint.h5')

    def board_to_tensor(self, board):
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

    def evaluate_reward(self, board):
        if board.is_checkmate():
            if board.result() == '1-0':
                return 1  # White wins
            elif board.result() == '0-1':
                return -1  # Black wins
            else:
                return 0  # Draw
        elif board.is_stalemate() or board.is_insufficient_material() or board.is_seventyfive_moves() or board.is_fivefold_repetition():
            return 0  # Draw
        else:
            return 0  # Ongoing game

    def discount_rewards(self, rewards):
        discounted = np.zeros_like(rewards, dtype=float)
        cumulative = 0.0
        for i in reversed(range(len(rewards))):
            cumulative = cumulative * self.gamma + rewards[i]
            discounted[i] = cumulative
        return discounted

if __name__ == '__main__':
    trainer = ChessAITrainer()
    trainer.train()
