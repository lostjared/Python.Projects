

class Token:
    def __init__(self):
        self.type = ""
        self.text = ""

    def add(self, ch):
        self.text += ch
    def print(self):
        print(self)

    def clear(self):
        self.text = ""

    def set_type(self, type):
        self.type = type
