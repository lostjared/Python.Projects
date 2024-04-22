
import token

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
            '==', '!=', '<=', '>=', '&&', '||', '++', '--', ',', '->*', '->', '()', '[]', '{}'
        ]
        for op in cpp_operators:
            for c in op:
                self.ch_map[c] = 3
        # Handle whitespace and similar characters
        self.ch_map[ord(' ')] = 0
        self.ch_map[ord('\t')] = 0
        self.ch_map[ord('\n')] = 0
        self.ch_map[ord('\r')] = 0

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
            self.token.set_type('OPERATOR')
            self.token.add(ch)

    def grab_id(self):
        while True:
            ch = self.peekchar()
            if ch is None or self.char_to_type(ch) != 1:
                break
            self.token.add(self.getchar())
        self.token.set_type('IDENTIFIER')

    def grab_digit(self):
        while True:
            ch = self.peekchar()
            if ch is None or self.char_to_type(ch) != 2:
                break
            self.token.add(self.getchar())
        self.token.set_type('NUMBER')

    def char_to_type(self, ch):
        if ch:
            return self.ch_map[ch] if ch in self.ch_map else 0
        return 0