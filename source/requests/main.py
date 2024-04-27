# requires requests
# pip install requests

import sys
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


def main(args):

    if len(args) != 2:
        print("Error requires argument", file=sys.stderr)
        return 1

    text = download(args[1])
    if text != None:
        print(text)
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
