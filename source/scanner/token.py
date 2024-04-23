

class Token:
    def __init__(self):
        self.type = ""
        self.text = ""
    def __init__(self, text, type):
        self.type = type
        self.text = text

    def add(self, ch):
        self.text += ch

    def print(self):
        print(self.text + " -> [ " + self.type + "]")

    def clear(self):
        self.text = ""
        self.type = ""

    def set_type(self, type):
        self.type = type
