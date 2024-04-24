
import token
import sys

class Scanner:
    def __init__(self, input):
        self.input = input
        self.token = None
        self.index = 0
        self.input_len = len(input)
        self.ch_map = dict()
        for i in range(0, 255):
            self.ch_map[chr(i)] = 0
        for i in range(ord('a'), ord('z') + 1):
            self.ch_map[chr(i)] = 1
        for i in range(ord('A'), ord('Z') + 1):
            self.ch_map[chr(i)] = 1
        for i in range(ord('0'), ord('9') + 1):
            self.ch_map[chr(i)] = 2
        cpp_operators = [
            '+', '-', '*', '/', '%', '^', '&', '|', '~', '!', '=', '<', '>', '+=',
            '-=', '*=', '/=', '%=', '^=', '&=', '|=', '<<', '>>', '>>=', '<<=',
            '==', '!=', '<=', '>=', '&&', '||', '++', '--', ',', '->*', '->', '()', '[]', '{}', '.', ';', ':'
        ]
        for op in cpp_operators:
            for c in op:
                self.ch_map[c] = 3

        self.multi_char = (
             '->', '++', '--', '<<', '>>', '&&', '||', '==', '!=', '<=', '>=', '+=', '-=', '*=', '/=', '%=', '&=', '|=', '^=', '<<=', '>>=', '->*', '::', '.*', '**', '***'
        )
        self.ch_map[' '] = 0
        self.ch_map['\t'] = 0
        self.ch_map['\n'] = 0
        self.ch_map['\r'] = 0
        self.ch_map['_'] = 1
        self.ch_map["\""] = 4
        self.ch_map['\''] = 5

    def error(self, s):
        print("Error: " + s)
        raise Exception
    
    def getchar(self):
        if self.index < self.input_len:
            ch = self.input[self.index]
            self.index += 1
            return ch
        return None

    def peekchar(self):
        if self.index < self.input_len:
            return self.input[self.index]
        return None

    def next(self):
        while self.index < self.input_len and self.char_to_type(self.peekchar()) == 0:
            self.index += 1  
        if self.index >= self.input_len:
            return None
        self.token = token.Token("", "")  
        self.grab_next()
        return self.token

    def grab_next(self):
        ch = self.getchar()
        if ch is None:
            return None
        type = self.char_to_type(ch)
        if type == 1:
            self.token.add(ch)
            self.grab_id()
        elif type == 2:
            self.token.add(ch)
            self.grab_digit()
        elif type == 3:
            self.token.set_type(3)
            self.token.add(ch)
            if self.char_to_type(self.peekchar()) == 3:
                self.grab_symbol()
        elif type == 4:
            self.token.set_type(4)
            self.grab_string()
        elif type == 5:
            self.token.set_type(5)
            self.grab_single()
        
    def grab_id(self):
        while True:
            ch = self.peekchar()
            if ch is None or (self.char_to_type(ch) != 1 and self.char_to_type(ch) != 2 and ch != '_'):
                break
            self.token.add(self.getchar())
        self.token.set_type(1)

    def grab_digit(self):
        count = 0
        while True:
            ch = self.peekchar()
            if ch == '.' and count > 0:
                self.error("Error multiple decimal points")
            if ch == '.' and count == 0:
                self.token.add(self.getchar())
                count += 1
                continue
            if ch is None or self.char_to_type(ch) != 2:
                break
            self.token.add(self.getchar())
        self.token.set_type(2)

    def grab_symbol(self):
        ch = self.peekchar()
        if self.char_to_type(ch) == 3:
            temp_op = self.token.text
            temp_op += ch
            if temp_op in self.multi_char:
                self.token.add(self.getchar())
                temp_op += self.peekchar()
                if temp_op in self.multi_char:
                    self.token.add(self.getchar())

    def grab_string(self):
        while True:
            ch = self.peekchar()
            if ch == None or ch == '\n' or ch == '\r':
                self.error("Missing closing quote")
                break
            if ch == '\\':
                self.token.add(self.getchar())
                self.token.add(self.getchar())
            elif self.char_to_type(ch) ==  4:
                ch = self.getchar()                
                return
            else:
                self.token.add(self.getchar())

    def grab_single(self):
        while True:
            ch = self.peekchar()
            if ch == None or ch == '\n' or ch == '\r':
                self.error("Missing closing single quote")
                break
            if ch == '\\':
                self.token.add(self.getchar())
                self.token.add(self.getchar())
            elif self.char_to_type(ch) == 5:
                ch = self.getchar()                
                return
            else:
                self.token.add(self.getchar())
                

    def char_to_type(self, ch):
        if ch:
            return self.ch_map[ch] if ch in self.ch_map else 0
        return 0