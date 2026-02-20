#!/usr/bin/env python3
import argparse
import random
import sys


def reverse_string(text: str) -> str:
    return text[::-1]


def shuffle_string(text: str) -> str:
    if len(text) < 4:
        return text
    first = text[0]
    last = text[-1]
    middle = list(text[1:-1])
    original_middle = middle[:]
    if all(c == middle[0] for c in middle):
        return text
    is_palindrome = text == text[::-1]
    attempts = 0
    while True:
        random.shuffle(middle)
        attempts += 1
        if attempts >= 1000:
            middle = original_middle
            break
        if middle != original_middle:
            break
    shuffled = first + "".join(middle) + last
    if not is_palindrome and shuffled == text:
        return text
    return shuffled


def parse_words(s: str, case_mode: int = 0) -> list[str]:
    words = []
    word = []
    for c in s:
        if c.isalpha():
            if case_mode == 0:
                word.append(c)
            elif case_mode == 1:
                word.append(c.upper())
            elif case_mode == 2:
                word.append(c.lower())
        else:
            if word:
                words.append("".join(word))
                word.clear()
    if word:
        words.append("".join(word))
    return words


def echo_words(words, func=None, sorted_output: bool = False):
    if func is not None:
        transformed = [func(w) for w in words]
        if sorted_output:
            transformed.sort()
        output = transformed
    else:
        output = list(words)
    print(" ".join(w for w in output if w))


def main():
    parser = argparse.ArgumentParser(description="Process words from a file")
    parser.add_argument("-s", "--shuffle", action="store_const", const=1, dest="mode", help="shuffle")
    parser.add_argument("-r", "--reverse", action="store_const", const=2, dest="mode", help="reverse")
    parser.add_argument("-n", "--noop", action="store_const", const=3, dest="mode", help="no operation keep the same")
    parser.add_argument("-c", "--static-order", action="store_true", help="static order (no shuffle)")
    parser.add_argument("-u", "--unique", action="store_true", help="unique words only")
    parser.add_argument("-o", "--sorted", action="store_true", help="sorted")
    parser.add_argument("-U", "--upper", action="store_const", const=1, dest="value_case", help="upper case")
    parser.add_argument("-L", "--lower", action="store_const", const=2, dest="value_case", help="lower case")
    parser.add_argument("-i", "--input", required=False, help="input file")

    args = parser.parse_args()

    if args.mode is None:
        print("You must provide an operation option", file=sys.stderr)
        parser.print_help()
        sys.exit(1)

    if args.value_case is None:
        args.value_case = 0

    if args.input is None:
        print("You must provide a filename", file=sys.stderr)
        parser.print_help()
        sys.exit(1)

    try:
        with open(args.input, "r") as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: file not found/could not open: {args.input}", file=sys.stderr)
        sys.exit(1)

    words = parse_words(content, args.value_case)

    if args.unique:
        words = list(dict.fromkeys(words))

    if not args.static_order:
        random.shuffle(words)

    if args.mode == 3:
        echo_words(words)
    else:
        func = reverse_string if args.mode == 2 else shuffle_string
        echo_words(words, func, args.sorted)


if __name__ == "__main__":
    main()
