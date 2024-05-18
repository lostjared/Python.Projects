#!/usr/bin/env python3

import os
import sys
    
class StringScan:
    def __init__(self, data=''):
        self.index = 0
        self.data = data
        self.dlen = len(data)

    @classmethod
    def zero(cls):
        return cls()

    @classmethod
    def new(cls, string_data):
        return cls(string_data)

    def getchar(self):
        if self.index < self.dlen:
            ch = self.data[self.index]
            self.index += 1
            return ch
        return None

    def curchar(self):
        return self.data[self.index]

    def peekchar(self, lookahead):
        if self.index + lookahead < self.dlen:
            return self.data[self.index + lookahead]
        return None

class XCsv:
    def __init__(self):
        self.scan = StringScan.zero()
        self.table = []

    def load_file(self, filename, sep):
        with open(filename, 'r') as f:
            self.load_string(f.read(), sep)

    def load_string(self, the_data, sep):
        for line in the_data.splitlines():
            self.scan = StringScan.new(line)
            result = self.tokenize(sep)
            if result is not None:
                self.table.append(result)

    def save_file(self, filename, sep):
        with open(filename, 'w') as f:
            for row in self.table:
                row_data = []
                for cell in row:
                    cell_str = ''
                    needs_quotes = sep in cell or '"' in cell or ' ' in cell
                    if needs_quotes:
                        cell_str += '"'
                        for ch in cell:
                            if ch == '"':
                                cell_str += '""'
                            else:
                                cell_str += ch
                        cell_str += '"'
                    else:
                        cell_str = cell
                    if cell_str:
                        row_data.append(cell_str)
                f.write(sep.join(row_data) + '\n')

    def add_row(self, data):
        data_row = [str(s) for s in data]
        self.table.append(data_row)

    def remove_row(self, row):
        self.table.pop(row)

    def at(self, row, col):
        return self.table[row][col]

    def not_token(ch, sep):
        return ch in (' ', '\r', '\n', '\t', sep)

    def grab_token(self, sep):
        if self.scan.index >= self.scan.dlen:
            return None

        if self.scan.curchar() == '"':
            data = ''
            self.scan.getchar()
            while True:
                ch = self.scan.getchar()
                if ch is not None:
                    if ch == '"':
                        next_c = self.scan.peekchar(0)
                        if next_c == '"':
                            data += '"'
                            self.scan.getchar()
                        else:
                            break
                    else:
                        data += ch
                else:
                    break
            return data
        else:
            data = ''
            while True:
                ch = self.scan.getchar()
                if ch is not None:
                    if not XCsv.not_token(ch, sep):
                        data += ch
                    else:
                        break
                else:
                    break
            return data

    def tokenize(self, sep):
        v = []
        while True:
            token = self.grab_token(sep)
            if token is not None:
                v.append(token)
            else:
                break
            c = self.scan.peekchar(0)
            if c == sep:
                self.scan.getchar()
        return v


def main(args):
    if len(sys.argv) != 2:
        print("incorrect arguments:\ncsv.py csv_file.csv", file=sys.stderr)
        sys.exit(1)
    
    # example usage
    xcsv = XCsv()
#load file
    xcsv.load_file(sys.argv[1], ',')
    #add a new row
    xcsv.add_row(["Apple", "Data", "Siren", "Thought"])
    #add another roww
    xcsv.add_row(["Turtle", "Duck", "Quck", "Meow"])
    #save modified csv file with ,   sas []
    xcsv.save_file("test1.txt", ',')

    #print out  patonm  Row(vertical) col (OIfozngal
    print("at(0,1) = " + xcsv.at(0, 1))
    print("at(2,2) + " + xcsv.at(2, 2))
    #for row in xcsv.table:
        #for i in row:
            #print(i)

if __name__ == "__main__":
    sys.exit(main(sys.argv))