
# RAW Image Converter

This script converts RAW image files (.rw2) to PNG or JPG formats. It reads the files you want to convert from a text file.

## Requirements

- `rawpy`
- `imageio`

## Installation

You can install the required libraries using pip:

```bash
pip install rawpy imageio
```

## Usage

Prepare a text file (e.g., `filelist.txt`) containing the paths of the RAW files you want to convert, each on a new line.
use
```bash
ls | egrep -i '.raw' > list.txt
or
ls | egrep -i '.rw2' > list.txt
```
to build the list file
### Running the Script

Use the following command to run the script:

```bash
python script.py filelist.txt output_format
```

- `filelist.txt`: The text file containing the list of RAW files to be converted.
- `output_format`: The desired output format (`png` or `jpg`).

### Example

```bash
python script.py filelist.txt png
```

## Notes

- Ensure the paths in `filelist.txt` are correct and accessible.
- The output files will be saved in the same directory as the source files with the specified format extension.

## Error Handling

The script includes basic error handling to manage file reading and writing issues. If an error occurs, it will print an error message and continue processing the next file.

