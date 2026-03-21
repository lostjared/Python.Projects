import sys

def print_words(words):
    for i in words.keys():
        print("Word: [" + i + "] = " + str(words[i]))

def count_words(string_value):
    i = 0
    word = ""
    words = dict()
    count = 0
    while i < len(string_value):
        c = string_value[i]
        if(c.isalnum()):
            word += c
        else:
            if len(word) > 0:
                words[word] = words.get(word, 0) + 1
                word = ""
                count = count + 1
        i += 1

    if len(word) > 0:
        words[word] = words.get(word, 0) + 1
        count = count + 1
    print_words(words)
    return count


def main():
    if len(sys.argv) <= 1:
        print("usage: count-words.py <filename>")
    else:
        for i in range(1, len(sys.argv)):
            filename = sys.argv[i]
            print("Counting words in: " + filename)
            try:
                with open(filename, 'r') as f:
                    text = f.read().lower()
                    words = count_words(text)
                    print("total count: " +  str(words))
            except FileNotFoundError:
                print("Error " + fiename + " not found")

if __name__ == "__main__":
    main()
