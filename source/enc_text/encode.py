import sys

def transform_char(c):
    if 'A' <= c <= 'Z':
        return chr(ord('Z') - (ord(c) - ord('A')))
    elif 'a' <= c <= 'z':
        return chr(ord('z') - (ord(c) - ord('a')))
    else:
        return c


def main(input_str):
    transformed = "".join([transform_char(c) for c in input_str])
    hex_list = [f"0x{ord(c):02x}" for c in transformed]
    hex_list.append("0x00")

    print("unsigned char values[] = {")
    print("    " + ", ".join(hex_list))
    print("};")

    sys.stdout.flush()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Error: No input string provided.")
        print("Usage: python3 encode.py \"your text here\"")
        sys.exit(1)

    input_value = sys.argv[1]
    main(input_value)
