# ChessBot

ChessBot es un bot de ajedrez que utiliza el motor de ajedrez Stockfish para jugar partidas. Este proyecto está dividido en dos partes: el backend (implementado con Flask) y el frontend (creado con React). El backend contiene la lógica de IA para tomar decisiones en el juego, y el frontend proporciona una interfaz gráfica para interactuar con el bot.

## Estructura del Proyecto

- `backend/` : Contiene el código del servidor Flask y la lógica de IA.
  - `app.py` : Archivo principal que ejecuta el servidor Flask.
  - `model.py`, `train.py`, `utils.py` : Scripts de la lógica de IA y utilidades.
- `frontend/` : Contiene el código del cliente en React.
  - `src/` : Código fuente de la aplicación de React.
  - `public/` : Archivos públicos de la aplicación.

## Prerrequisitos

Asegúrate de tener Docker y Docker Compose instalados en tu sistema.

## Instalación y Ejecución

1. Clona el repositorio.
2. Construye las imágenes Docker y ejecuta los contenedores con el siguiente comando:

   ```bash
   docker-compose up --build
