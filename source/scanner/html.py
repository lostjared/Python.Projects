# pip install requests
# for http download
# scan for HTML tags
import sys
import scanner
import scan_token
import requests

class Tag:
    def __init__(self, type, tokens):
        self.type = type
        self.tokens = tokens
    def __str__(self):
        text = self.type
        text += " - ["
        for i in range(0, len(self.tokens)-1):
            text += self.tokens[i].text + ", "
        text += self.tokens[len(self.tokens)-1].text
        text += "]"
        return text
    

def download(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  
        return response.text
    except requests.exceptions.HTTPError as errh:
        print("HTTP Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        print("OOps: Something Else", err)
    return None

def scan(url):
    text = download(url)
    if text != None:
        scan = scanner.Scanner(text, err_on=False)
        tokens = list()
        tags = list()
        try: 
            while scan.next():
                tokens.append(scan_token.Token(scan.token.text, scan.token.type))
                scan.token.clear()
        except Exception:
            print ("Scanner: Syntax Error")
            sys.exit(1)

        return tokens
    return None

def main(args):
    if len(args) >= 2:
        tokens = scan(args[1])
        if tokens != None:
            index = 0
            tags = list()
            while index < len(tokens):
                token = tokens[index]
                if token.text == "<":
                    if index+1 < len(tokens):
                        index += 1
                        type = tokens[index].text
                        if type == "/" and index +1 < len(tokens):
                            type = "/" + tokens[index+1].text 
                        if type == "!" and index+1 < len(tokens):
                            type  = "!" + tokens[index+1].text    
                        tok_list = []
                        while index < len(tokens) and tokens[index].text != ">":
                            tok_list.append(tokens[index])
                            index += 1
                        tag = Tag(type, tok_list)
                        tags.append(tag)
                index += 1
            for i in tags:
                print(i)
        else:
            print("requires one argument txt file")

if __name__ == "__main__":
    sys.exit(main(sys.argv))