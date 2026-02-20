#!/usr/bin/env python3
import sys
import time
import random


def echo_line_vector(lines: list[str], milli: int):
    for line in lines:
        for ch in line:
            print(ch, end="", flush=True)
            time.sleep(milli / 1000.0)
        print(" ", end="", flush=True)


def main():
    if len(sys.argv) != 4:
        print("Error incorrect arguments.", file=sys.stderr)
        print("Use: input_tex_file.txt delay mode", file=sys.stderr)
        sys.exit(1)

    filename = sys.argv[1]
    milli = int(sys.argv[2])
    mode = int(sys.argv[3])

    if mode not in (1, 2):
        print("Error missing mode (0 or 1)")
        sys.exit(1)

    if milli == 0:
        print("Invalid delay", file=sys.stderr)
        sys.exit(1)

    try:
        with open(filename, "r") as f:
            raw_lines = f.readlines()
    except FileNotFoundError:
        print(f"Error open file: {filename}", file=sys.stderr)
        sys.exit(1)

    lines: list[str] = []
    for line in raw_lines:
        line = line.rstrip("\n")
        if mode == 1:
            lines.append(line)
        elif mode == 2:
            lines.extend(line.split())

    # repeat until break with Ctrl+C
    while True:
        echo_line_vector(lines, milli)
        if mode == 2:
            random.shuffle(lines)


if __name__ == "__main__":
    main()
