
# Remember Words Recall Game

This Python-based game challenges players to recall and type words presented to them in a limited amount of time. Utilizing SDL2 and SDL2_ttf libraries, the game offers a simple graphical interface for an engaging memory test.

## Prerequisites

To run this game, you need to have Python installed on your system along with the SDL2 and SDL2_ttf libraries. The game is developed and tested with Python 3.8.

### Dependencies

- Python 3.8 or above
- PySDL2: A wrapper around the SDL2 library which provides functions for working directly with SDL2 within Python.
- SDL2_ttf: A library for using TrueType fonts in SDL applications.

You can install PySDL2 and SDL2_ttf using pip:

```bash
pip install pysdl2 pysdl2-dll
```

For SDL2_ttf, you may need to download and install the library from the SDL2 website or use a package manager depending on your operating system.


## Running the Game

To start the game, navigate to the directory containing the game files and run:

```bash
python remember.py
```

## Gameplay Overview

- **Start Screen**: Press `Space` to start the game.
- **Game Mode**: Words will appear one by one. After each word, press `Enter` to start a countdown timer.
- **Recall Mode**: Type the words that were displayed, in the correct order, before time runs out.
- **End Game**: The game will show whether the recalled words were correct or incorrect. Press `Space` to restart or `Esc` to exit.

## Game Controls

- `Space`: Start the game or continue to the next round.
- `Enter`: Start the countdown for word recall.
- `Backspace`: Correct your input while recalling words.
- `Esc`: Exit the game.

## License

This project is licensed under the GPLv3 License - see the LICENSE file for details.

## Contributions

Contributions are welcome! Please open an issue or submit a pull request with your improvements.
