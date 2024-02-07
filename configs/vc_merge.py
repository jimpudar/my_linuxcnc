import sys
import re

def halui_tokens(filename):
    try:
        with open(filename, 'r') as file:
            for line in file:
                matches = re.finditer(r'(halui[a-zA-Z0-9.-]+)|net ([a-zA-Z0-9.-]+)', line)
                for match in matches:
                    yield match.group()
    except FileNotFoundError:
        print(f"The file {filename} was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def comment_line_matching_token(multiline_string, token):
    lines = multiline_string.split('\n')
    commented_lines = ['#' + line if token in line and not line.lstrip().startswith('#') else line for line in lines]
    return '\n'.join(commented_lines)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python vc_merge.py vc-p4s.hal <your-halfile>.hal")
        sys.exit(1)

    vc_filename = sys.argv[1]
    machine_filename = sys.argv[2]

    with open(machine_filename, 'r') as machine_file:
        machine_hal = machine_file.read()

        for halui_token in halui_tokens(vc_filename):
            machine_hal = comment_line_matching_token(machine_hal, halui_token)
        
        print(machine_hal)
