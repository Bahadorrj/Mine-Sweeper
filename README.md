# Minesweeper with AI

A Python implementation of the classic Minesweeper game, enhanced with an AI player that learns and deduces safe moves to intelligently play the game. The AI uses logical inference to mark cells as safe or as mines and makes random moves when necessary.<br> This repository is one of the projects in CS50 AI with Python course.

## Features

- **Classic Minesweeper Gameplay**: Play the traditional game on an `8x8` grid.
- **AI Player**: 
  - Learns from each move and builds a knowledge base.
  - Deduces safe moves and mines based on game rules.
  - Makes random moves only when no guaranteed safe moves are available.
- **Customizable Grid**: Adjust the size of the game grid.

## How It Works

The AI leverages logical inference through the following mechanisms:
1. **Knowledge Base**: Stores sentences about the state of the game, including:
   - Which cells are safe.
   - Which cells contain mines.
2. **Marking Safe/Mine Cells**: Based on the information provided by the game, the AI deduces which neighboring cells are safe or contain mines.
3. **Move Decision**:
   - Chooses a move known to be safe.
   - If no safe moves are available, chooses a random cell that is not already a known mine.

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/minesweeper-ai.git
cd minesweeper-ai
```
Ensure Python 3.x is installed on your system.
Install any dependencies:
```bash
pip install -r requirements.txt 
```

## How to Play
Run the game:

```bash
python runner.py
```