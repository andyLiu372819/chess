# Chess

A pygame-based chess project. The current version renders a chess board from a compact board-state string and displays the starting position. This repo is the starting point for building a full playable chess game first, then a chess engine later.

## Current Features

- 8x8 chess board rendered with pygame
- Starting chess position represented in FEN-like notation
- Board drawing handled by a dedicated `Board` class
- Piece image assets included under `img/pieces/`

## Project Structure

```text
main.py       Starts the pygame window and game loop
board.py      Stores board dimensions and draws the board state
img/pieces/   Chess piece image assets
```

## Run The Game

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the game:

```bash
python main.py
```

## Roadmap

The next steps for the chess game are:

- Convert the board state into a stronger internal data model
- Draw actual piece sprites instead of text labels
- Add piece selection and movement
- Validate legal moves
- Add turn tracking
- Detect check, checkmate, and stalemate
- Add special rules: castling, en passant, and promotion

After the game rules are complete, this project can grow into a chess engine with board evaluation, minimax search, and alpha-beta pruning.
