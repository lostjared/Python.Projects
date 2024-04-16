# Puzzle Game [Python Edition]

## Overview
This project is a puzzle game implemented in Python using the SDL2 library for graphical rendering. Players control falling puzzle pieces, aiming to align colors to score points and speed up the gameplay. The game features real-time rendering and event handling, providing a challenging and engaging experience.

## Requirements
- Python 3.x
- PySDL2
- SDL2
- SDL2_ttf (for font rendering)

## Installation
Before running the game, you must install the PySDL2 library and ensure that SDL2 and SDL2_ttf are available on your system.

### Installing PySDL2
```bash
pip install pysdl2 pysdl2-dll
```

### Setting up SDL2 Libraries
Ensure that SDL2 and SDL2_ttf libraries are correctly installed and configured on your system. This may involve downloading the libraries from the SDL website and placing them in your system's library path.

## Usage
Run the game by executing the script with Python. Ensure that the necessary font file (`font.ttf`) is present in your script's directory or specify the path to the font.

### Running the Game
```bash
python main.py
```

## Key Features
- Real-time puzzle piece handling and rendering.
- Score tracking and game speed adjustments based on player performance.
- Simple graphical user interface using SDL2.

## Controls
- **Arrow Left/Right**: Move the puzzle piece left or right.
- **Arrow Up**: Rotate the puzzle piece.
- **Arrow Down**: Speed up the puzzle piece descent.
- **Enter**: Start a new game after game over.

## Contributing
Contributions to this project are welcome! Please fork the repository, make your changes, and submit a pull request.

## License
This project is released under the GPLv3 License.
