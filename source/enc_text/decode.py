import sys
import re

def transform_char(c):
    if 'A' <= c <= 'Z':
        return chr(ord('Z') - (ord(c) - ord('A')))
    elif 'a' <= c <= 'z':
        return chr(ord('z') - (ord(c) - ord('a')))
    else:
        return c


def decode_hex_string(hex_input):
    hex_pattern = re.compile(r'0x[0-9a-fA-F]+')
    matches = hex_pattern.findall(hex_input)

    decoded_chars = []

    for h in matches:
        val = int(h, 16)
        if val == 0:
            break

        original_char = transform_char(chr(val))
        decoded_chars.append(original_char)

    return "".join(decoded_chars)


if __name__ == "__main__":
    if len(sys.argv) < 2: pass
    else:
        data = sys.argv[1]
        result = decode_hex_string(data)
        print(f"Hex Input: {data}")
        print(f"Decoded:   {result}")
