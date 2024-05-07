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

        file_types = { ".c": ["C", 0, 0], ".cpp":["C++", 0, 0],".hpp":["C++", 0, 0], ".h":["C/C++ header", 0, 0],".m":["Objective-C",0, 0], ".mm":["Objective-C++",0, 0], ".cc":["C++",0, 0], ".py":["Python", 0, 0], ".rs": ["Rust",0, 0] }

        for i in files:
            lower_type = i.lower()
            if lower_type.endswith((".cpp", ".hpp", ".c", ".h", ".m", ".mm", ".cc", ".py", ".rs")):
                f_type = lower_type[lower_type.rfind("."):]
                value = count_lines(i)
                print("%s:[%s] lines: [%d] blanks [%d] total [%d]" % (file_types[f_type][0], i, value[0], value[1], value[2]))
                line_number += value[0]
                blank_lines += value[1]
                file_types[f_type][1] += value[0]
                file_types[f_type][2] += value[1]

        print("lines %d , blanks %d, total %d" % (line_number, blank_lines, line_number + blank_lines))

        for i in file_types.keys():
            if file_types[i][1] > 0:
                print("%d lines %d blanks %d total of %s in project" % ( file_types[i][1], file_types[i][2], file_types[i][1]+file_types[i][2], file_types[i][0] ) )

    else:
        print("arguments: dir")

if __name__ == "__main__":
    sys.exit(main(sys.argv))