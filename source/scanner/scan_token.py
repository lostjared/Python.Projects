

class Token:
    def __init__(self, text, type):
        self.type = type
        self.text = text
        self.type_id = 0

    def add(self, ch):
        self.text += ch

    def print(self):
        print(self.text + " -> [" + self.type_to_string(self.type) + "]")

    def clear(self):
        self.text = ""
        self.type = ""

    def __str__(self):
        return self.text + " -> [" + self.type_to_string(self.type) + "]"

    def type_to_string(self, type):
        match type:
            case 1:
                return "IDENTIFIER"
            case 2:
                return "NUMBER"
            case 3:
                return "OPERATOR"
            case 4:
                return "STRING"
            case 5:
                return "SINGLE QUOTE STRING"
        return None

    def set_type(self, type):
        self.type = type

