#!/usr/bin/env python3
import sys
import os

def proc_directory(directory):
    file_list = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_list.append(os.path.join(root, file))
    return file_list

def is_blank(data):
    return not data.strip()  

def count_lines(filename):
    line_number = 0
    blank_lines = 0
    with open(filename, encoding="utf-8", errors="ignore") as fp:
        for line in fp:
            temp_line = line.strip()
            if is_blank(temp_line):
                blank_lines += 1
            else:
                line_number += 1
    return line_number, blank_lines, line_number + blank_lines

def main(args):
    if len(args) >= 2:
        files = proc_directory(args[1])
        line_number = 0
        blank_lines = 0
        for i in files:
            if i.endswith((".cpp", ".hpp", ".c", ".h", ".m", ".mm", ".cc", ".py", ".rs")):
                value = count_lines(i)
                print(" file [%s] lines: [%d] blanks [%d] total [%d]" % (i, value[0], value[1], value[2]))
                line_number += value[0]
                blank_lines += value[1]
        print("lines %d , blanks %d, total %d" % (line_number, blank_lines, line_number + blank_lines))
    else:
        print("arguments: dir")

if __name__ == "__main__":
    sys.exit(main(sys.argv))