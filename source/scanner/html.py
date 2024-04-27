# pip install requests
# for http download

import sys
import scanner
import scan_token
import requests

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
            for i in tokens:
                i.print()
        else:
            print("requires one argument txt file")

if __name__ == "__main__":
    sys.exit(main(sys.argv))