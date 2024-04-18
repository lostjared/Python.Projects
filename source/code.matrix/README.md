
# Matrix Falling Text Simulation


![matriximg](https://github.com/lostjared/Python.Projects/blob/main/screens/matrix.jpg "Matrix")

This project is a Python-based simulation that mimics the iconic falling text effect seen in the "Matrix" film series. It utilizes the SDL2 library along with SDL2_ttf for rendering text. The simulation displays characters that randomly change and move vertically across the screen in a continuous loop.

## Requirements

- Python 3.x
- PySDL2
- SDL2
- SDL2_ttf (a part of SDL2)

Make sure SDL2 and SDL2_ttf are installed and properly configured on your system. You can download them from the [SDL website](https://www.libsdl.org/) or use a package manager suitable for your operating system.

## Installation

1. Clone this repository or download the source code.
2. Ensure that the SDL2 and SDL2_ttf libraries are installed on your system.

## Usage

To run the simulation, navigate to the directory containing the script and run:

```bash
python matrix.py
```

Ensure you have a suitable font file named `font.ttf` in the same directory as the script or modify the `font_path` in the `XObject` class to point to a valid font file on your system.

## Features

- Dynamic text effects inspired by the "Matrix" movies.
- Characters fall at different speeds and change direction based on user input (Up and Down arrow keys).
- Simple font and color configuration.

## Configuration

You can customize the behavior of the falling text by modifying parameters in the script:
- Change the `font_path` to use different fonts.
- Adjust the color of the text by modifying the RGB values in `build_character_list`.

## Controls

- `UP Arrow`: Changes the direction of the falling text to move upwards.
- `DOWN Arrow`: Changes the direction of the falling text to move downwards.
- `ESC`: Exits the program.

## License

This project is open-sourced under the GPLv3 license.
Feel free to use and modify this code. If you encounter any issues or have suggestions for improvements, please open an issue or submit a pull request.
