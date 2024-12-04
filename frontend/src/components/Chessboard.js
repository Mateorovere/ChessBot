import React, { useState, useEffect } from 'react';
import Chessboard from 'chessboardjsx';
import { Chess } from 'chess.js';
import axios from 'axios';
import { Github, Linkedin } from 'lucide-react';
import './ChessboardComponent.css';

const ChessboardComponent = () => {
  const [game, setGame] = useState(new Chess());
  const [fen, setFen] = useState('start');
  const [gameOver, setGameOver] = useState(false);
  const [resultMessage, setResultMessage] = useState('');
  const [statusMessage, setStatusMessage] = useState('');

  useEffect(() => {
    const timer = setTimeout(() => setStatusMessage(''), 3000);
    return () => clearTimeout(timer);
  }, [statusMessage]);

  const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:5000';

  const onDrop = async ({ sourceSquare, targetSquare, piece }) => {
    if (gameOver) return;

    const move = {
      from: sourceSquare,
      to: targetSquare,
      promotion: 'q',
    };

    try {
      const legalMove = game.move(move);
      if (legalMove === null) {
        setStatusMessage('Invalid move. Try again.');
        return;
      }

      setFen(game.fen());

      if (isGameOver(game)) {
        handleGameOver();
        return;
      }

      const response = await axios.post(`${BACKEND_URL}/move`, {
        fen: game.fen(),
      });
      
      if (response.data && response.data.fen) {
        game.load(response.data.fen);
        setFen(game.fen());

        if (isGameOver(game)) {
          handleGameOver();
        }
      } else {
        console.error('Invalid response from server:', response);
        setStatusMessage('Error: Invalid response from server');
      }
    } catch (error) {
      console.error('Error:', error);
      setStatusMessage('Server error. Please try again.');
    }
  };

  const isGameOver = (chess) => {
    return chess.isGameOver() || chess.isCheckmate() || chess.isDraw();
  };

  const handleGameOver = () => {
    setGameOver(true);
    if (game.isCheckmate()) {
      setResultMessage(game.turn() === 'w' ? 'Black wins!' : 'White wins!');
    } else if (game.isDraw()) {
      setResultMessage('Draw!');
    } else if (game.isStalemate()) {
      setResultMessage('Stalemate!');
    } else if (game.isThreefoldRepetition()) {
      setResultMessage('Draw by repetition!');
    } else if (game.isInsufficientMaterial()) {
      setResultMessage('Draw due to insufficient material!');
    } else {
      setResultMessage('Game over!');
    }
  };

  const resetGame = () => {
    const newGame = new Chess();
    setGame(newGame);
    setFen('start');
    setGameOver(false);
    setResultMessage('');
    setStatusMessage('');
  };

  return (
    <div className="chess-container">
      <div className="chess-content">
        <h1>Grandmaster AI</h1>
        <div className="chessboard-wrapper">
          <Chessboard
            width={350}
            position={fen}
            onDrop={onDrop}
            draggable={!gameOver}
            boardStyle={{
              borderRadius: "5px",
              boxShadow: "0 5px 15px rgba(0, 0, 0, 0.5)"
            }}
          />
        </div>
        {statusMessage && (
          <div className="message status-message">{statusMessage}</div>
        )}
        {resultMessage && (
          <div className="message result-message">{resultMessage}</div>
        )}
        {gameOver && (
          <button onClick={resetGame} className="reset-button">
            New Game
          </button>
        )}
        <footer>
          <div className="social-links">
            <a
              href="https://github.com/Mateorovere"
              target="_blank"
              rel="noopener noreferrer"
            >
              <Github size={24} />
            </a>
            <a
              href="https://www.linkedin.com/in/mateo-rovere/"
              target="_blank"
              rel="noopener noreferrer"
            >
              <Linkedin size={24} />
            </a>
          </div>
          <p>Created by Mateo Rovere</p>
        </footer>
      </div>
    </div>
  );
};

export default ChessboardComponent;